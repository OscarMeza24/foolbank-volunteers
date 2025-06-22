<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TestSupabaseController;

Route::post('/insert-data', [TestSupabaseController::class, 'simpleInsert'])->name('simple.insert');
