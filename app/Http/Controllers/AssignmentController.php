<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\SupabaseService;
use App\Services\VolunteerMatchingService;
use App\Models\Assignment;
use App\Models\Event;

const required = 'required';
const nullable = 'nullable';
const string = 'string';
const uuid = 'uuid';
const in = 'in';

class AssignmentController extends Controller
{
    protected $supabaseService;
    protected $volunteerMatchingService;

    public function __construct(
        SupabaseService $supabaseService,
        VolunteerMatchingService $volunteerMatchingService
    ) {
        $this->supabaseService = $supabaseService;
        $this->volunteerMatchingService = $volunteerMatchingService;
    }

    public function index()
    {
        try {
            $assignments = $this->supabaseService->query('assignments', [
                'select' => '*'
            ]);
            return response()->json($assignments);
        } catch (\Exception $e) {
            return response()->json([
                'error' => $e->getMessage()
            ], 500);
        }
    }

    public function show($id)
    {
        try {
            $assignment = $this->supabaseService->query('assignments', [
                'select' => '*',
                'id' => $id
            ]);
            return response()->json($assignment);
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
                'volunteer_id' => required . '|uuid',
                'event_id' => required . '|uuid',
                'role' => required . '|string',
                'status' => required . '|string|in:assigned,confirmed,completed,cancelled',
                'assigned_by' => required . '|uuid'
            ]);

            $data['id'] = $this->supabaseService->generateUUID();
            $result = $this->supabaseService->insert('assignments', $data);
            
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
                'role' => nullable . '|string',
                'status' => nullable . '|string|in:assigned,confirmed,completed,cancelled'
            ]);

            $result = $this->supabaseService->update('assignments', $id, $data);
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
            $result = $this->supabaseService->delete('assignments', $id);
            return response()->json($result);
        } catch (\Exception $e) {
            return response()->json([
                'error' => $e->getMessage()
            ], 500);
        }
    }

    public function assign(Event $event)
    {
        $assignments = $this->volunteerMatchingService->matchVolunteersToEvent($event);
        return response()->json(['assignments' => $assignments]);
    }

    public function confirmAssignment(Assignment $assignment)
    {
        $assignment->status = 'confirmed';
        $assignment->save();
        return response()->json(['message' => 'Assignment confirmed']);
    }

    public function rejectAssignment(Assignment $assignment)
    {
        $assignment->status = 'rejected';
        $assignment->save();
        return response()->json(['message' => 'Assignment rejected']);
    }
}
