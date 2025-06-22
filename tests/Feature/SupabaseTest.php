<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\Hash;
use Tests\TestCase;
use App\Models\User;

class SupabaseTest extends TestCase
{
    /**
     * Test de conexión con Supabase
     */
    public function test_supabase_connection()
    {
        try {
            // Primero iniciar sesión como administrador
            $admin = User::factory()->create([
                'email' => uniqid('admin1_', true) . '@example.com',
                'password' => Hash::make('password123'),
                'is_admin' => true
            ]);
            
            $this->actingAs($admin);

            // Verificar que el usuario se creó correctamente
            $this->assertDatabaseHas('users', [
                'email' => $admin->email
            ]);

            $response = $this->get('/api/v1/test/connection');
            
            // Verificar el estado de la respuesta
            $this->assertEquals(200, $response->getStatusCode(), 'La respuesta no tiene el código de estado esperado');
            
            // Verificar el contenido de la respuesta
            $content = json_decode($response->getContent(), true);
            $this->assertIsArray($content, 'La respuesta no es un JSON válido');
            
            // Verificar los campos específicos
            $this->assertTrue($content['success'], 'El campo success no es true');
            $this->assertEquals('Conexión exitosa con Supabase', $content['message'], 'El mensaje no coincide');
            
            // Verificar la estructura completa
            $this->assertArrayHasKey('success', $content);
            $this->assertArrayHasKey('message', $content);
            
        } catch (\Exception $e) {
            // Log del error para depuración
            $this->fail('Error en el test: ' . $e->getMessage());
        }
    }

    protected function setUp(): void
    {
        parent::setUp();
        
        // Limpiar la base de datos entre pruebas
        $this->artisan('migrate:fresh --force --env=testing');
    }

    /**
     * Test de registro de usuario
     */
    public function test_user_signup()
    {
        // Primero iniciar sesión como administrador
        $admin = User::factory()->create([
            'email' => uniqid('admin2_', true) . '@example.com',
            'password' => Hash::make('password123'),
            'is_admin' => true
        ]);
        
        $this->actingAs($admin);

        $userData = [
            'email' => uniqid('test_', true) . '@example.com',
            'password' => 'password123',
            'password_confirmation' => 'password123',
            'first_name' => 'Test',
            'last_name' => 'User'
        ];

        $response = $this->postJson('/api/v1/test/signup', $userData);
        $response->assertStatus(200);
        $response->assertJson([
            'success' => true,
            'message' => 'Usuario registrado exitosamente'
        ]);

        // Verificar que la respuesta tenga el formato correcto
        $response->assertJsonStructure([
            'success',
            'message'
        ]);
    }

    /**
     * Test de inserción de datos
     */
    public function test_data_insert()
    {
        // Primero iniciar sesión como administrador
        $admin = User::factory()->create([
            'email' => uniqid('admin3_', true) . '@example.com',
            'password' => Hash::make('password123'),
            'is_admin' => true
        ]);
        
        $this->actingAs($admin);

        // Crear un usuario para usar su ID
        $user = User::factory()->create();
        
        $data = [
            'table' => 'volunteer_profiles',
            'data' => [
                'user_id' => $user->id,
                'availability' => json_encode(['full_time' => true]),
                'skills' => [], // Array vacío por defecto
                'has_transport' => false, // Booleano por defecto
                'reliability_score' => 0.8, // Número por defecto
                'total_hours_volunteered' => 0 // Entero por defecto
            ]
        ];

        // Intentar insertar los datos
        $response = $this->postJson('/api/v1/test/insert', $data);
        $response->assertStatus(200);
        $response->assertJson([
            'success' => true,
            'message' => 'Datos insertados exitosamente'
        ]);

        // Verificar que los datos se guardaron correctamente
        $queryResponse = $this->getJson('/api/v1/test/connection');
        $queryResponse->assertStatus(200);
        
        // Verificar que el voluntario existe
        $volunteers = json_decode($queryResponse->content(), true);
        $found = false;
        foreach ($volunteers as $volunteer) {
            if ($volunteer['user_id'] == $user->id && 
                in_array('cooking', $volunteer['skills']) && 
                $volunteer['availability'] == 'full_time') {
                $found = true;
                break;
            }
        }
        
        $this->assertTrue($found, 'El voluntario no se encontró en la base de datos');
    }
}
