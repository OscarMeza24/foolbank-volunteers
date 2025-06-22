<?php

namespace Tests\Feature;

use Tests\TestCase;
use Illuminate\Support\Facades\Config;

class SupabaseConfigTest extends TestCase
{
    /**
     * Test de configuración de Supabase
     */
    public function test_supabase_config()
    {
        // Verificar que las variables de entorno están configuradas
        $this->assertNotEmpty(env('SUPABASE_URL'), 'SUPABASE_URL no está configurado');
        $this->assertNotEmpty(env('SUPABASE_KEY'), 'SUPABASE_KEY no está configurado');
        
        // Verificar que la configuración de Supabase está siendo cargada
        $config = Config::get('supabase');
        $this->assertNotEmpty($config['url'], 'URL de Supabase no configurada');
        $this->assertNotEmpty($config['key'], 'Key de Supabase no configurada');
        $this->assertIsBool($config['verify_ssl'], 'verify_ssl debe ser booleano');
    }
}
