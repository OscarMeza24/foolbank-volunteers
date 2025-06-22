<?php

namespace App\Http\Controllers;

use App\Services\SupabaseService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Auth;

class TestSupabaseController extends Controller
{
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
                throw new \Exception('Error al consultar Supabase: ' . $response->getStatusCode());
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
    
    public function signup(Request $request)
    {
        try {
            // Validar los datos del request
            $validated = $request->validate([
                'email' => 'required|email|unique:users',
                'password' => 'required|min:8|confirmed',
                'password_confirmation' => 'required|min:8',
                'first_name' => 'required|string|max:50',
                'last_name' => 'required|string|max:50'
            ]);

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

            if ($response->getStatusCode() !== 200) {
                throw new \Exception('Error al registrar usuario: ' . $response->getStatusCode());
            }

            // Obtener el ID del usuario recién creado
            $userId = $response['user']['id'] ?? null;
            
            if (!$userId) {
                throw new \Exception('No se pudo obtener el ID del usuario');
            }

            return response()->json([
                'success' => true,
                'message' => 'Usuario registrado exitosamente',
                'user_id' => $userId
            ]);

        } catch (\Exception $e) {
            Log::error('Supabase signup error: ' . $e->getMessage());
            return response()->json([
                'success' => false,
                'message' => 'Error al registrar usuario: ' . $e->getMessage()
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

            if ($response->getStatusCode() !== 201) {
                throw new \Exception('Error al insertar datos: ' . $response->getStatusCode());
            }

            // Obtener los datos insertados
            $insertedData = json_decode($response->getBody(), true);

            return response()->json([
                'success' => true,
                'message' => 'Datos insertados exitosamente',
                'data' => $insertedData
            ]);

        } catch (\Exception $e) {
            Log::error('Supabase insert error: ' . $e->getMessage());
            return response()->json([
                'success' => false,
                'message' => 'Error al insertar datos: ' . $e->getMessage()
            ], 500);
        }
    }

    private function validateDataStructure($table, $data)
    {
        switch ($table) {
            case 'users':
                if (!isset($data['email']) || !isset($data['password'])) {
                    throw new \Exception('Los campos email y password son requeridos para usuarios ...');
                }
                break;
            case 'volunteers':
                if (!isset($data['user_id']) || !isset($data['skills'])) {
                    throw new \Exception('Los campos user_id y skills son requeridos para voluntarios ...');
                }
                break;
            case 'assignments':
                if (!isset($data['volunteer_id']) || !isset($data['event_id'])) {
                    throw new \Exception('Los campos volunteer_id y event_id son requeridos para asignaciones ...');
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
            
            if ($response->getStatusCode() !== 201) {
                throw new \Exception('Error al insertar datos: ' . $response->getStatusCode());
            }
            
            return response()->json([
                'success' => true,
                'message' => 'Datos insertados exitosamente',
                'data' => json_decode($response->getBody(), true)
            ]);
            
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error: ' . $e->getMessage()
            ], 500);
        }
    }
}
