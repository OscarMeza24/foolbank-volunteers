<?php

namespace App\Http\Middleware;

use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

class VerifyCsrfToken extends Middleware
{
    /**
     * The URIs that should be excluded from CSRF verification.
     *
     * @var array<int, string>
     */
    protected $except = [
        'test-insert',
        'test-supabase',
        'signup',
        'test.signup',
        'api/v1/test/*'
    ];

    protected function tokensMatch($request)
    {
        if ($request->isMethod('POST') && 
            ($request->is('signup') || $request->is('test-signup'))) {
            return true;
        }
        return parent::tokensMatch($request);
    }
}
