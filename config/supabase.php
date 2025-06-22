<?php

return [
    'url' => env('SUPABASE_URL'),
    'key' => env('SUPABASE_KEY'),
    'verify_ssl' => env('APP_ENV') === 'local' ? false : true,
];
