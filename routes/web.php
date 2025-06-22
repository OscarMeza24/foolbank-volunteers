<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\VolunteerController;
use App\Http\Controllers\EventController;
use App\Http\Controllers\AssignmentController;
use App\Http\Controllers\TestController;
use App\Http\Controllers\TestSupabaseController;
use App\Http\Controllers\UserController;

// Rutas públicas
Route::get('/', function () {
    return view('welcome');
});

// Ruta simple para pruebas
Route::post('/simple', function (Illuminate\Http\Request $request) {
    return response()->json([
        'success' => true,
        'message' => 'Datos recibidos',
        'data' => $request->all()
    ]);
});

// Ruta de prueba simple para verificar conexión de Laravel
Route::get('/test', [TestController::class, 'index'])->name('test');

// Ruta para crear usuario de prueba (solo en desarrollo)
Route::get('/create-test-user', [UserController::class, 'createTestUser'])
    ->middleware('test')
    ->name('test.user.create');

// Rutas protegidas por autenticación
Route::middleware(['auth'])->group(function () {
    // Rutas de Volunteer
    Route::resource('volunteers', VolunteerController::class);
    Route::post('volunteers/recommendations', [VolunteerController::class, 'recommendEvents'])->name('volunteers.recommendations');

    // Rutas de Event
    Route::resource('events', EventController::class);
    Route::post('events/{event}/recommend-volunteers', [EventController::class, 'recommendVolunteers'])->name('events.recommend-volunteers');
    Route::post('events/{event}/assign-volunteer', [EventController::class, 'assignVolunteer'])->name('events.assign-volunteer');

    // Rutas de Assignment
    Route::resource('assignments', AssignmentController::class);
});

// Rutas de autenticación
Route::get('login', [\App\Http\Controllers\Auth\LoginController::class, 'showLoginForm'])->name('login');
Route::post('login', [\App\Http\Controllers\Auth\LoginController::class, 'login']);
Route::post('logout', [\App\Http\Controllers\Auth\LoginController::class, 'logout'])->name('logout');

// Ruta de registro
Route::get('register', [\App\Http\Controllers\Auth\RegisterController::class, 'showRegistrationForm'])->name('register');
Route::post('register', [\App\Http\Controllers\Auth\RegisterController::class, 'register']);

// Ruta para restablecer contraseña
Route::get('password/reset', function () {
    return view('auth.passwords.email');
})->name('password.request');

// Ruta para crear usuario de prueba
Route::get('/create-test-user', [UserController::class, 'createTestUser'])->name('test.user.create');
