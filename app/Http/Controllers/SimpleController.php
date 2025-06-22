<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class SimpleController extends Controller
{
    public function insert(Request $request)
    {
        return response()->json(['message' => 'Datos recibidos', 'data' => $request->all()]);
    }
}