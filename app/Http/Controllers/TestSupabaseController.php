<?php

namespace App\Http\Controllers;

use App\Services\SupabaseService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

use App\Rules\SupabaseValidationRules;
use App\Exceptions\SupabaseException;
use Illuminate\Http\JsonResponse;
use App\Contracts\SupabaseResponse;
use Psr\Http\Message\ResponseInterface;

class TestSupabaseController extends Controller
{
    private function getErrorInsertMessage(): string
    {
        return 'Error al insertar datos';
    }
    protected $supabaseService;

    public function __construct(SupabaseService $supabaseService)
    {
        $this->supabaseService = $supabaseService;
    }

    public function testConnection(Request $request)
    {
        try {
            // Log para verificar la configuración del servicio
            Log::info('Supabase connection test - Base URL: ' . $this->supabaseService->getBaseUrl());
            Log::info('Supabase connection test - API Key: ' . substr($this->supabaseService->getApiKey(), 0, 5) . '...' . substr($this->supabaseService->getApiKey(), -5));
            
            // Intentar hacer una consulta simple a Supabase
            try {
                $response = $this->supabaseService->query('volunteer_profiles', [
                    'select' => 'id',
                    'limit' => 1
                ]);

                Log::info('Supabase connection test - Response status: ' . $response->getStatusCode());
                Log::info('Supabase connection test - Response body: ' . $response->getBody());

                return response()->json([
                    'success' => true,
                    'message' => 'Conexión exitosa con Supabase'
                ]);
            } catch (\GuzzleHttp\Exception\ConnectException $e) {
                // Error específico de conexión
                Log::error('Error de conexión con Supabase: ' . $e->getMessage());
                return response()->json([
                    'success' => false,
                    'message' => 'No se pudo conectar con Supabase. Verifica la URL y las credenciales.',
                    'error' => [
                        'type' => get_class($e),
                        'message' => $e->getMessage()
                    ]
                ], 500);
            } catch (\GuzzleHttp\Exception\RequestException $e) {
                // Error en la petición
                Log::error('Error en la petición a Supabase: ' . $e->getMessage());
                return response()->json([
                    'success' => false,
                    'message' => 'Error en la petición a Supabase.',
                    'error' => [
                        'type' => get_class($e),
                        'message' => $e->getMessage(),
                        'response' => $e->getResponse() ? $e->getResponse()->getBody()->getContents() : null
                    ]
                ], 500);
            } catch (\Exception $e) {
                // Error general
                Log::error('Error general en Supabase: ' . $e->getMessage());
                return response()->json([
                    'success' => false,
                    'message' => 'Error en la conexión con Supabase.',
                    'error' => [
                        'type' => get_class($e),
                        'message' => $e->getMessage()
                    ]
                ], 500);
            }
        } catch (\Exception $e) {
            // Error en la inicialización del servicio
            Log::error('Error al inicializar el servicio Supabase: ' . $e->getMessage());
            return response()->json([
                'success' => false,
                'message' => 'Error al inicializar el servicio Supabase.',
                'error' => [
                    'type' => get_class($e),
                    'message' => $e->getMessage()
                ]
            ], 500);
        }
    }
    
    /**
     * @param \Illuminate\Http\Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function signup(Request $request)
    {
        try {
            // Validar los datos del request
            $validated = $request->validate(
                SupabaseValidationRules::userSignUpRules(),
                SupabaseValidationRules::errorMessages()
            );

            // Crear datos adicionales para el usuario
            $userData = [
                'first_name' => $validated['first_name'],
                'last_name' => $validated['last_name']
            ];

            // Registrar usuario en Supabase
            $response = $this->supabaseService->signup(
                $validated['email'],
                $validated['password'],
                $userData
            );

            if ($response['status'] !== 200) {
                throw SupabaseException::fromResponse($response);
            }

            // Obtener el ID del usuario recién creado
            $userData = $response['user'] ?? null;
            if (!$userData) {
                throw SupabaseException::fromMessage('No se recibieron datos del usuario');
            }
            
            $userId = $userData['id'] ?? null;
            if (!$userId) {
                throw SupabaseException::fromMessage('No se pudo obtener el ID del usuario');
            }
            
            if (!$userId) {
                throw SupabaseException::fromMessage('No se pudo obtener el ID del usuario');
            }

            /**
             * Devuelve una respuesta JSON con el resultado del registro del usuario.
             *
             * @return \Illuminate\Http\JsonResponse
             */
            return response()->json([
                'success' => true,
                'message' => 'Usuario registrado exitosamente',
                'user_id' => $userId
            ]);

        } catch (\Exception $e) {
            Log::error('Supabase signup error: ' . $e->getMessage());
            return response()->json([
                'success' => false,
                'message' => $this->getErrorInsertMessage() . ': ' . $e->getMessage()
            ], 500);
        }
    }

    public function testInsert(Request $request)
    {
        try {
            // Validar los datos del request
            $validated = $request->validate([
                'table' => 'required|string',
                'data' => 'required|array',
                'table' => 'in:volunteer_profiles' // Solo permitir la tabla volunteer_profiles para este test
            ]);

            // Validar estructura de datos
            $requiredFields = ['user_id', 'availability'];
            $optionalFields = ['skills', 'has_transport', 'reliability_score', 'total_hours_volunteered'];
            
            // Validar campos requeridos
            foreach ($requiredFields as $field) {
                if (!isset($validated['data'][$field])) {
                    throw new \Exception("El campo {$field} es requerido para el perfil de voluntario");
                }
            }

            // Validar tipos de datos
            if (isset($validated['data']['skills'])) {
                if (!is_array($validated['data']['skills'])) {
                    throw new \Exception('El campo skills debe ser un array');
                }
            }
            if (isset($validated['data']['has_transport'])) {
                if (!is_bool($validated['data']['has_transport'])) {
                    throw new \Exception('El campo has_transport debe ser booleano');
                }
            }
            if (isset($validated['data']['reliability_score'])) {
                if (!is_numeric($validated['data']['reliability_score'])) {
                    throw new \Exception('El campo reliability_score debe ser numérico');
                }
            }
            if (isset($validated['data']['total_hours_volunteered'])) {
                if (!is_numeric($validated['data']['total_hours_volunteered'])) {
                    throw new \Exception('El campo total_hours_volunteered debe ser numérico');
                }
            }

            // Preparar datos para inserción
            $insertData = [
                'user_id' => $validated['data']['user_id'],
                'availability' => $validated['data']['availability']
            ];

            // Agregar campos opcionales si existen
            foreach ($optionalFields as $field) {
                if (isset($validated['data'][$field])) {
                    $insertData[$field] = $validated['data'][$field];
                }
            }

            // Procesar la inserción en Supabase
            $response = $this->supabaseService->insert($validated['table'], $validated['data']);

            if ($response['status'] !== 201) {
                throw SupabaseException::fromResponse($response);
            }

            // Obtener los datos insertados
            $insertedData = json_decode($response['body'], true);

            return response()->json([
                'success' => true,
                'message' => 'Datos insertados exitosamente',
                'data' => $insertedData
            ]);

        } catch (\Exception $e) {
            Log::error('Supabase insert error: ' . $e->getMessage());
            return response()->json([
                'success' => false,
                'message' => $this->getErrorInsertMessage() . ': ' . $e->getMessage()
            ], 500);
        }
    }

    private function validateDataStructure($table, $data)
    {
        switch ($table) {
            case 'users':
                if (!isset($data['email']) || !isset($data['password'])) {
                    throw new \Exception('Los campos email y password son requeridos para usuarios');
                }
                break;
            case 'volunteers':
                if (!isset($data['user_id']) || !isset($data['skills'])) {
                    throw new \Exception('Los campos user_id y skills son requeridos para voluntarios');
                }
                break;
            case 'assignments':
                if (!isset($data['volunteer_id']) || !isset($data['event_id'])) {
                    throw new \Exception('Los campos volunteer_id y event_id son requeridos para asignaciones');
                }
                break;
            default:
                throw new \Exception('Tabla no soportada');
        }
    }

    private function validateCsrfToken(Request $request)
    {
        $token = $request->header('X-CSRF-TOKEN');
        
        if (!$token || !csrf_token() || $token !== csrf_token()) {
            throw new \Exception('Token CSRF inválido');
        }
    }

    public function simpleInsert(Request $request)
    {
        try {
            $data = $request->all();
            
            // Insertar en la tabla volunteers
            $response = $this->supabaseService->insert('volunteers', $data);
            
            if ($response['status'] !== 201) {
                throw SupabaseException::fromResponse($response);
            }
            
            $body = json_decode($response['body'], true);
            if (!is_array($body)) {
                throw SupabaseException::fromMessage('Respuesta no válida de Supabase');
            }
            
            return response()->json([
                'success' => true,
                'message' => 'Datos insertados exitosamente',
                'data' => $body
            ]);
            
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => $this->getErrorInsertMessage() . ': ' . $e->getMessage()
            ], 500);
        }
    }
}