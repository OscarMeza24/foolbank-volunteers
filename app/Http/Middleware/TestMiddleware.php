<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class TestMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next)
    {
        // Permitir acceso solo en entorno de desarrollo
        if (app()->environment('testing', 'local')) {
            return $next($request);
        }

        return response()->json([
            'success' => false,
            'message' => 'Esta ruta solo está disponible en entorno de desarrollo'
        ], 403);
    }
}
