<?php

namespace App\Services;

use GuzzleHttp\Client as GuzzleClient;
use Ramsey\Uuid\Uuid;
use Illuminate\Support\Facades\Log;

class SupabaseService
{
    protected $client;
    protected $baseUrl;
    protected $authBaseUrl;
    protected $apiKey;
    protected $verifySSL;

    public function __construct()
    {
        $config = config('supabase');
        
        if (empty($config['url']) || empty($config['key'])) {
            throw new \Exception('Las credenciales de Supabase no están configuradas correctamente');
        }

        $this->baseUrl = $config['url'];
        $this->authBaseUrl = $this->baseUrl . '/auth/v1';
        $this->apiKey = $config['key'];
        $this->verifySSL = $config['verify_ssl'];

        $this->client = new GuzzleClient([
            'base_uri' => $this->baseUrl,
            'headers' => [
                'apikey' => $this->apiKey,
                'Authorization' => 'Bearer ' . $this->apiKey,
                'Content-Type' => 'application/json'
            ],
            'verify' => $this->verifySSL
        ]);
    }

    public function getClient()
    {
        return $this->client;
    }

    public function signup($email, $password, $data = [])
    {
        try {
            $response = $this->client->request('POST', $this->authBaseUrl . '/signup', [
                'headers' => [
                    'apikey' => $this->apiKey,
                    'Authorization' => 'Bearer ' . $this->apiKey
                ],
                'json' => [
                    'email' => $email,
                    'password' => $password,
                    'data' => $data,
                    'options' => [
                        'email_redirect_to' => env('APP_URL') . '/auth/callback'
                    ]
                ]
            ]);
            
            $body = $response->getBody();
            $content = $body->getContents();
            
            Log::info('Supabase signup response: ' . $content);
            
            $result = json_decode($content, true);
            
            if (isset($result['error'])) {
                throw new \Exception($result['error'] ?? 'Error al registrar usuario');
            }
            
            return $result;
        } catch (\Exception $e) {
            // Mostrar el error completo en el log
            Log::error('Supabase signup error: ' . $e->getMessage());
            throw $e;
        }
    }

    public function login($email, $password)
    {
        try {
            // Intentar iniciar sesión con Supabase
            $response = $this->client->request('POST', $this->authBaseUrl . '/token?grant_type=password', [
                'headers' => [
                    'apikey' => $this->apiKey,
                    'Authorization' => 'Bearer ' . $this->apiKey
                ],
                'json' => [
                    'email' => $email,
                    'password' => $password
                ]
            ]);

            $body = $response->getBody();
            $content = $body->getContents();
            
            // Mostrar la respuesta completa en el log para depuración
            Log::info('Supabase login response: ' . $content);
            
            $result = json_decode($content, true);
            
            // Verificar si hay un error en la respuesta
            if (isset($result['error_code'])) {
                if ($result['error_code'] === 'invalid_credentials') {
                    throw new \Exception('Las credenciales proporcionadas no son válidas. Por favor, verifica tu correo y contraseña.');
                } elseif ($result['error_code'] === 'unconfirmed') {
                    throw new \Exception('Por favor, verifica tu correo electrónico para iniciar sesión.');
                }
            }

            // Verificar si el usuario está verificado
            if (!isset($result['user']['confirmed_at'])) {
                throw new \Exception('Por favor, verifica tu correo electrónico para iniciar sesión.');
            }

            return $result;
        } catch (\Exception $e) {
            // Mostrar el error completo en el log
            Log::error('Supabase login error: ' . $e->getMessage());
            throw new \Exception('Error al iniciar sesión: ' . $e->getMessage());
        }
    }

    public function query($table, $params = [])
    {
        try {
            $response = $this->client->request('GET', '/rest/v1/' . $table, [
                'query' => $params
            ]);
            
            return $response;
        } catch (\Exception $e) {
            Log::error('Supabase query error: ' . $e->getMessage());
            throw $e;
        }
    }

    public function select($columns = '*')
    {
        return ['select' => $columns];
    }

    public function eq($field, $value)
    {
        return [$field => $value];
    }

    public function insert($table, $data)
    {
        if (empty($table)) {
            throw new \Exception('El nombre de la tabla es requerido');
        }

        if (!is_array($data)) {
            throw new \Exception('Los datos deben ser un array');
        }

        try {
            $response = $this->client->request('POST', '/rest/v1/' . $table, [
                'json' => $data
            ]);

            if ($response->getStatusCode() !== 201) {
                throw new \Exception('Error al insertar datos: ' . $response->getStatusCode());
            }

            return $response;

        } catch (\Exception $e) {
            Log::error('Supabase insert error: ' . $e->getMessage());
            throw new \Exception('Error al insertar datos');
        }
    }

    public function update($table, $id, $data)
    {
        if (empty($table)) {
            throw new \Exception('El nombre de la tabla es requerido');
        }

        if (empty($id)) {
            throw new \Exception('El ID es requerido');
        }

        if (!is_array($data)) {
            throw new \Exception('Los datos deben ser un array');
        }

        try {
            $response = $this->client->request('PATCH', $table . '?id=eq.' . $id, [
                'headers' => [
                    'apikey' => $this->apiKey,
                    'Authorization' => 'Bearer ' . $this->apiKey,
                    'Content-Type' => 'application/json'
                ],
                'json' => $data
            ]);

            $body = $response->getBody();
            $content = $body->getContents();
            
            // Validar la respuesta
            if ($response->getStatusCode() !== 200) {
                throw new \Exception('Error al actualizar datos');
            }

            return json_decode($content, true);

        } catch (\Exception $e) {
            Log::error('Supabase update error: ' . $e->getMessage());
            throw new \Exception('Error al actualizar datos');
        }
    }

    public function delete($table, $id)
    {
        if (empty($table)) {
            throw new \Exception('El nombre de la tabla es requerido');
        }

        if (empty($id)) {
            throw new \Exception('El ID es requerido');
        }

        try {
            $response = $this->client->request('DELETE', $table . '?id=eq.' . $id, [
                'headers' => [
                    'apikey' => $this->apiKey,
                    'Authorization' => 'Bearer ' . $this->apiKey
                ]
            ]);

            // Validar la respuesta
            if ($response->getStatusCode() !== 204) {
                throw new \Exception('Error al eliminar datos');
            }

            return true;

        } catch (\Exception $e) {
            Log::error('Supabase delete error: ' . $e->getMessage());
            throw new \Exception('Error al eliminar datos');
        }
    }

    public function getVolunteerData($userId)
    {
        return $this->query('volunteers', [
            'select' => '*',
            'user_id' => $userId
        ]);
    }

    public function getEventVolunteers($eventId)
    {
        return $this->query('assignments', [
            'select' => '*',
            'volunteers!inner(*)',
            'event_id' => $eventId
        ]);
    }

    public function createVolunteer(array $data)
    {
        $data['id'] = $this->generateUUID();
        return $this->insert('volunteers', $data);
    }

    public function createEvent(array $data)
    {
        $data['id'] = $this->generateUUID();
        return $this->insert('events', $data);
    }

    public function createAssignment(array $data)
    {
        $data['id'] = $this->generateUUID();
        return $this->insert('assignments', $data);
    }

    public function generateUUID(): string
    {
        return (string) \Ramsey\Uuid\Uuid::uuid4();
    }
}
