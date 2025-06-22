<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class DatabaseConnectionTest extends TestCase
{
    /**
     * Test para verificar la conexión a la base de datos SQLite
     *
     * @return void
     */
    public function test_database_connection()
    {
        try {
            // Intentar hacer una consulta simple
            $result = DB::select('SELECT 1 + 1 as result');
            
            // Verificar que la consulta devolvió un resultado
            $this->assertNotEmpty($result);
            $this->assertEquals(2, $result[0]->result);
            
            // Intentar crear una tabla temporal para verificar escritura
            DB::statement('CREATE TEMPORARY TABLE test_table (id INTEGER PRIMARY KEY)');
            
            // Insertar un registro
            DB::statement('INSERT INTO test_table (id) VALUES (1)');
            
            // Verificar que el registro se insertó correctamente
            $count = DB::table('test_table')->count();
            $this->assertEquals(1, $count);
            
            // Eliminar la tabla temporal
            DB::statement('DROP TABLE test_table');
            
            $this->assertTrue(true, 'Conexión a la base de datos exitosa');
        } catch (\Exception $e) {
            $this->fail("Error al conectar con la base de datos: " . $e->getMessage());
        }
    }
}
