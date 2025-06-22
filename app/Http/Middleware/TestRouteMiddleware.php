<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class TestRouteMiddleware
{
    public function handle(Request $request, Closure $next)
    {
        // Verificar si la aplicación está en modo producción
        if (app()->environment('production')) {
            return response()->json([
                'success' => false,
                'message' => 'Rutas de prueba no disponibles en producción'
            ], 403);
        }

        // Verificar que el usuario esté autenticado
        if (!Auth::check()) {
            return response()->json([
                'success' => false,
                'message' => 'Autenticación requerida'
            ], 401);
        }

        return $next($request);
    }
}
