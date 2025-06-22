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

    public function testConnection()
    {
        try {
            // Intentar una consulta básica para verificar conexión
            $response = $this->supabaseService->query('volunteers', [
                'select' => '*'
            ]);
            
            if ($response->getStatusCode() !== 200) {
                throw SupabaseException::fromResponse($response);
            }
            
            $data = json_decode($response->getBody(), true);
            
            return response()->json([
                'success' => true,
                'message' => 'Conexión exitosa con Supabase',
                'data' => $data
            ]);
        } catch (\Exception $e) {
            Log::error('Supabase connection error: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'message' => 'Error al conectar con Supabase: ' . $e->getMessage()
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
                'table' => 'in:users,volunteers,assignments' // Solo permitir tablas específicas
            ]);

            // Validar estructura de datos según la tabla
            $this->validateDataStructure($validated['table'], $validated['data']);

            // Procesar la inserción en Supabase
            $response = $this->supabaseService->insert($validated['table'], $validated['data']);

            if ($response['status'] !== 201) {
                throw SupabaseException::fromResponse($response);
            }

            // Obtener los datos insertados
            $insertedData = json_decode($response['body'], true);

            /**
             * Devuelve una respuesta JSON con el resultado de la inserción.
             *
             * @return \Illuminate\Http\JsonResponse
             */
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
            /** @var \Psr\Http\Message\ResponseInterface $response */
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
