<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\SupabaseService;

class VolunteerController extends Controller
{
    protected $supabaseService;

    public function __construct(SupabaseService $supabaseService)
    {
        $this->supabaseService = $supabaseService;
    }

    public function index()
    {
        try {
            $volunteers = $this->supabaseService->query('volunteers', [
                'select' => '*'
            ]);
            return response()->json($volunteers);
        } catch (\Exception $e) {
            return response()->json([
                'error' => $e->getMessage()
            ], 500);
        }
    }

    public function show($id)
    {
        try {
            $volunteer = $this->supabaseService->query('volunteers', [
                'select' => '*',
                'id' => $id
            ]);
            return response()->json($volunteer);
        } catch (\Exception $e) {
            return response()->json([
                'error' => $e->getMessage()
            ], 500);
        }
    }

    public function store(Request $request)
    {
        try {
            $data = $request->validate([
                'user_id' => 'required|uuid',
                'skills' => 'nullable|array',
                'availability' => 'required|array',
                'has_transport' => 'boolean',
                'reliability_score' => 'numeric|min:0|max:1',
                'total_hours_volunteered' => 'integer|min:0'
            ]);

            $data['id'] = $this->supabaseService->generateUUID();
            $result = $this->supabaseService->insert('volunteers', $data);
            
            return response()->json($result, 201);
        } catch (\Exception $e) {
            return response()->json([
                'error' => $e->getMessage()
            ], 500);
        }
    }

    public function update(Request $request, $id)
    {
        try {
            $data = $request->validate([
                'skills' => 'nullable|array',
                'availability' => 'required|array',
                'has_transport' => 'boolean',
                'reliability_score' => 'numeric|min:0|max:1',
                'total_hours_volunteered' => 'integer|min:0'
            ]);

            $result = $this->supabaseService->update('volunteers', $id, $data);
            return response()->json($result);
        } catch (\Exception $e) {
            return response()->json([
                'error' => $e->getMessage()
            ], 500);
        }
    }

    public function destroy($id)
    {
        try {
            $result = $this->supabaseService->delete('volunteers', $id);
            return response()->json($result);
        } catch (\Exception $e) {
            return response()->json([
                'error' => $e->getMessage()
            ], 500);
        }
    }
}
