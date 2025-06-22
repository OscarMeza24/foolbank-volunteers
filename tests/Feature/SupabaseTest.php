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
        // Primero iniciar sesión como administrador
        $admin = User::factory()->create([
            'email' => uniqid('admin1_', true) . '@example.com',
            'password' => Hash::make('password123'),
            'is_admin' => true
        ]);
        
        $this->actingAs($admin);

        $response = $this->get('/api/v1/test/connection');
        $response->assertStatus(200);
        $response->assertJson([
            'success' => true,
            'message' => 'Conexión exitosa con Supabase'
        ]);

        // Verificar que la respuesta tenga el formato correcto
        $response->assertJsonStructure([
            'success',
            'message'
        ]);
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
            'table' => 'volunteers',
            'data' => [
                'user_id' => $user->id,
                'skills' => ['cooking', 'organizing'],
                'availability' => 'full_time'
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
