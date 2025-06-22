<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Services\SupabaseService;
use Illuminate\Support\Facades\Log;
use App\Models\User;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    protected $supabaseService;

    public function __construct(SupabaseService $supabaseService)
    {
        $this->supabaseService = $supabaseService;
    }

    public function showLoginForm()
    {
        return view('auth.login');
    }

    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        try {
            // Intentar iniciar sesión con Supabase
            $response = $this->supabaseService->login(
                $request->email,
                $request->password
            );

            // Mostrar la respuesta en el log para depuración
            Log::info('Login response: ' . json_encode($response));

            // Verificar si el login fue exitoso
            if (isset($response['user'])) {
                // Obtener los datos del usuario
                $userData = $response['user'];
                
                // Buscar o crear el usuario en Laravel
                $user = User::firstOrCreate(
                    ['email' => $userData['email']],
                    [
                        'first_name' => $userData['user_metadata']['first_name'] ?? 'Usuario',
                        'last_name' => $userData['user_metadata']['last_name'] ?? '',
                        'user_type' => 'volunteer',  // Por defecto, todos son voluntarios
                        'password' => bcrypt($userData['password'] ?? ''),  // Hash de la contraseña
                    ]
                );

                // Iniciar sesión usando el método correcto de Laravel
                Auth::login($user);
                $request->session()->regenerate();
                
                // Guardar el token de Supabase en la sesión
                $request->session()->put('supabase_token', $response['access_token']);
                
                return redirect()->intended('/');
            }

            return back()->withErrors([
                'email' => 'Las credenciales proporcionadas no coinciden con nuestros registros.',
            ]);
        } catch (\Exception $e) {
            // Mostrar el error completo en el log
            Log::error('Login error: ' . $e->getMessage());
            
            // Mostrar mensaje de error más descriptivo
            if (strpos($e->getMessage(), 'invalid_credentials') !== false) {
                return back()->withErrors([
                    'email' => 'Las credenciales proporcionadas no son válidas. Por favor, verifica tu correo y contraseña.',
                ]);
            } elseif (strpos($e->getMessage(), 'unconfirmed') !== false) {
                return back()->withErrors([
                    'email' => 'Por favor, verifica tu correo electrónico para iniciar sesión.',
                ]);
            }
            
            return back()->withErrors([
                'email' => 'Error al iniciar sesión: ' . $e->getMessage(),
            ]);
        }
    }

    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect('/');
    }
}
