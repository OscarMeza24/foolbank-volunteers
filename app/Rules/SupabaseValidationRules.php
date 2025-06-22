<?php

namespace App\Rules;

abstract class SupabaseValidationRules
{
    const REQUIRED = 'required';
    const NULLABLE = 'nullable';
    const STRING = 'string';
    const UUID = 'uuid';
    const IN = 'in';
    const EMAIL = 'email';
    const UNIQUE = 'unique';
    const MIN = 'min';
    const MAX = 'max';
    const CONFIRMED = 'confirmed';

    public static function userSignUpRules(): array
    {
        return [
            'email' => self::REQUIRED . '|' . self::EMAIL . '|' . self::UNIQUE . ':users',
            'password' => self::REQUIRED . '|' . self::MIN . ':8|' . self::CONFIRMED,
            'password_confirmation' => self::REQUIRED . '|' . self::MIN . ':8',
            'first_name' => self::REQUIRED . '|' . self::STRING . '|' . self::MAX . ':50',
            'last_name' => self::REQUIRED . '|' . self::STRING . '|' . self::MAX . ':50'
        ];
    }

    public static function errorMessages(): array
    {
        return [
            'email.unique' => 'El correo electrónico ya está registrado',
            'password.min' => 'La contraseña debe tener al menos 8 caracteres',
            'password.confirmed' => 'Las contraseñas no coinciden',
            'first_name.max' => 'El nombre no puede exceder 50 caracteres',
            'last_name.max' => 'El apellido no puede exceder 50 caracteres'
        ];
    }
}
