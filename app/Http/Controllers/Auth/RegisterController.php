<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Services\SupabaseService;
use Illuminate\Support\Facades\Log;

class RegisterController extends Controller
{
    protected $supabaseService;

    public function __construct(SupabaseService $supabaseService)
    {
        $this->supabaseService = $supabaseService;
    }

    public function showRegistrationForm()
    {
        return view('auth.register');
    }

    public function register(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255',
            'password' => 'required|string|min:8|confirmed',
        ]);

        try {
            // 1. Registrar el usuario
            $signupResponse = $this->supabaseService->signup(
                $request->email,
                $request->password,
                ['name' => $request->name]
            );

            // Mostrar la respuesta de registro en el log
            Log::info('Registro exitoso: ' . json_encode($signupResponse));

            // Verificar si el registro requiere verificación de correo
            if (isset($signupResponse['error_code']) && $signupResponse['error_code'] === 'email_already_confirmed') {
                return back()->withErrors([
                    'email' => 'Este correo electrónico ya está registrado. Por favor, inicia sesión.'
                ]);
            }

            // Mostrar mensaje de éxito y explicar que se necesita verificar el correo
            return back()->with('success', 'Registro exitoso! Por favor, verifica tu correo electrónico para completar el registro.');

        } catch (\Exception $e) {
            // Mostrar el error en el log
            Log::error('Error al registrar: ' . $e->getMessage());
            return back()->withErrors([
                'email' => 'Error al registrar: ' . $e->getMessage()
            ]);
        }

    }
}
