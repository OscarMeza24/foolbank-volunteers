<?php

namespace App\Contracts;

interface SupabaseResponse
{
    public function getBody(): string;
    public function getStatusCode(): int;
    public function toArray(): array;
}
