<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TestSupabaseController;

// Ruta para probar conexión con Supabase
Route::prefix('v1')->group(function () {
    // Ruta para probar conexión con Supabase
    Route::get('/test/connection', [TestSupabaseController::class, 'testConnection'])
        ->name('api.test.connection');

    // Ruta de registro de prueba
    Route::post('/test/signup', [TestSupabaseController::class, 'signup'])
        ->name('api.test.signup');

    // Ruta para probar inserción de datos
    Route::post('/test/insert', [TestSupabaseController::class, 'testInsert'])
        ->name('api.test.insert');
});
