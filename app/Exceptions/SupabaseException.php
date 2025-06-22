<?php

namespace App\Exceptions;

use Exception;

class SupabaseException extends Exception
{
    public static function fromResponse($response)
    {
        $statusCode = $response->getStatusCode();
        $message = 'Error al procesar la solicitud: ' . $statusCode;
        
        if ($response->getBody()) {
            try {
                $error = json_decode($response->getBody(), true);
                $message = $error['message'] ?? $message;
            } catch (Exception $e) {
                // Si hay error al decodificar JSON, usar el mensaje base
            }
        }
        
        return new static($message, $statusCode);
    }

    public static function fromMessage(string $message, int $code = 500)
    {
        return new static($message, $code);
    }
}
