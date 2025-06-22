<?php

namespace App\Services;

use GuzzleHttp\Client as GuzzleClient;
use Ramsey\Uuid\Uuid;
use Illuminate\Support\Facades\Log;
use App\Exceptions\SupabaseException;
use App\Contracts\SupabaseResponse;

class SupabaseService
{
    protected $client;
    protected $baseUrl;
    protected $authBaseUrl;
    protected $apiKey;
    protected $verifySSL;

    public function getBaseUrl(): string
    {
        return $this->baseUrl;
    }

    public function getApiKey(): string
    {
        return $this->apiKey;
    }

    public function __construct()
    {
        $this->initializeConfig();
        $this->initializeClient();
    }

    private function initializeConfig(): void
    {
        $config = config('supabase');
        
        if (empty($config['url']) || empty($config['key'])) {
            throw SupabaseException::fromMessage('Las credenciales de Supabase no están configuradas correctamente');
        }

        $this->baseUrl = $config['url'];
        $this->authBaseUrl = $this->baseUrl . '/auth/v1';
        $this->apiKey = $config['key'];
        $this->verifySSL = $config['verify_ssl'] ?? true;

        // Log de configuración para depuración
        Log::info('Supabase service initialized');
        Log::info('Supabase URL: ' . $this->baseUrl);
        Log::info('Supabase API Key (partial): ' . substr($this->apiKey, 0, 5) . '...' . substr($this->apiKey, -5));
    }

    private function initializeClient(): void
    {
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

    /**
     * @return array
     */
    public function signup(string $email, string $password, array $data = [])
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
            // Verificar que la tabla existe
            if (empty($table)) {
                throw new \Exception('El nombre de la tabla es requerido');
            }

            // Construir la URL completa
            $url = $this->baseUrl . '/rest/v1/' . $table;
            
            // Agregar headers de autenticación explícitamente
            $headers = [
                'apikey' => $this->apiKey,
                'Authorization' => 'Bearer ' . $this->apiKey,
                'Content-Type' => 'application/json',
                'Accept' => 'application/json'
            ];

            // Verificar si estamos en entorno de prueba
            if (env('APP_ENV') === 'testing') {
                // En entorno de prueba, usar SSL verification=false
                $headers['verify'] = false;
            }

            // Realizar la petición
            $response = $this->client->request('GET', $url, [
                'headers' => $headers,
                'query' => $params,
                'timeout' => 30, // Aumentar timeout para pruebas
                'connect_timeout' => 10
            ]);
            
            // Verificar el estado de la respuesta
            $statusCode = $response->getStatusCode();
            Log::info('Supabase query response status: ' . $statusCode);
            
            // Obtener el cuerpo de la respuesta
            $body = $response->getBody()->getContents();
            Log::info('Supabase query response body: ' . $body);
            
            // Verificar si es JSON válido
            $json = json_decode($body, true);
            if (json_last_error() !== JSON_ERROR_NONE) {
                throw new \Exception('Respuesta no válida de Supabase: ' . json_last_error_msg());
            }
            
            return $response;
        } catch (\GuzzleHttp\Exception\ConnectException $e) {
            // Error de conexión específica
            Log::error('Error de conexión con Supabase: ' . $e->getMessage());
            throw new \Exception('No se pudo conectar con Supabase. Verifica la URL y las credenciales.');
        } catch (\GuzzleHttp\Exception\RequestException $e) {
            // Error en la petición
            Log::error('Error en la petición a Supabase: ' . $e->getMessage());
            throw new \Exception('Error en la petición a Supabase: ' . $e->getMessage());
        } catch (\Exception $e) {
            // Error general
            Log::error('Error general en Supabase: ' . $e->getMessage());
            throw new \Exception('Error en la conexión con Supabase: ' . $e->getMessage());
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
            // Agregar headers de autenticación explícitamente
            $response = $this->client->request('POST', '/rest/v1/' . $table, [
                'headers' => [
                    'apikey' => $this->apiKey,
                    'Authorization' => 'Bearer ' . $this->apiKey,
                    'Content-Type' => 'application/json',
                    'Prefer' => 'return=representation'
                ],
                'json' => $data
            ]);

            Log::info('Supabase insert response status: ' . $response->getStatusCode());
            Log::info('Supabase insert response body: ' . $response->getBody());

            if ($response->getStatusCode() !== 201) {
                throw SupabaseException::fromResponse($response);
            }

            $body = json_decode($response->getBody()->getContents(), true);
            if (!is_array($body)) {
                throw SupabaseException::fromMessage('Respuesta no válida de Supabase');
            }
            
            return new class($body) implements SupabaseResponse {
                private $body;
                
                public function __construct(array $body)
                {
                    $this->body = $body;
                }
                
                public function getBody(): string
                {
                    return json_encode($this->body);
                }
                
                public function getStatusCode(): int
                {
                    return 201;
                }
                
                public function toArray(): array
                {
                    return $this->body;
                }
            };

        } catch (\Exception $e) {
            Log::error('Supabase insert error: ' . $e->getMessage());
            Log::error('Supabase insert error type: ' . get_class($e));
            Log::error('Supabase insert error code: ' . $e->getCode());
            Log::error('Supabase insert error file: ' . $e->getFile());
            Log::error('Supabase insert error line: ' . $e->getLine());
            Log::error('Supabase insert error trace: ' . $e->getTraceAsString());
            throw $e;
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
