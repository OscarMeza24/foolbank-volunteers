<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TestSupabaseController;

Route::prefix('api/test')->group(function () {
    Route::get('/connection', [TestSupabaseController::class, 'testConnection'])->name('test.connection');
    Route::post('/signup', [TestSupabaseController::class, 'signup'])->name('test.signup');
    Route::post('/insert', [TestSupabaseController::class, 'testInsert'])->name('test.insert');
});
