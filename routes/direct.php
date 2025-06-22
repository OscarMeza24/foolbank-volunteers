<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\SimpleController;

Route::post('/simple-insert', [SimpleController::class, 'insert'])->name('simple.insert');
