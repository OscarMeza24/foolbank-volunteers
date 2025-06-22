<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\SupabaseService;
use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Auth;


class EventController extends Controller
{
    protected $supabaseService;

    protected $middleware = ['auth'];

    public function __construct(SupabaseService $supabaseService)
    {
        $this->supabaseService = $supabaseService;
    }

    public function index()
    {
        try {
            $events = $this->supabaseService->query('events', [
                'select' => '*'
            ]);
            return view('events.index', compact('events'));
        } catch (\Exception $e) {
            return back()->withErrors(['error' => $e->getMessage()]);
        }
    }

    public function show($id)
    {
        try {
            $event = $this->supabaseService->query('events', [
                'select' => '*',
                'id' => $id
            ]);
            return view('events.show', compact('event'));
        } catch (\Exception $e) {
            return back()->withErrors(['error' => $e->getMessage()]);
        }
    }

    public function store(Request $request)
    {
        try {
            $data = $request->validate([
                'name' => 'required|string|max:255',
                'event_type' => 'required|string|in:collection,distribution,awareness,fundraising',
                'start_date' => 'required|date',
                'end_date' => 'required|date|after:start_date',
                'location' => 'required|string',
                'required_volunteers' => 'required|integer|min:1',
                'status' => 'required|string|in:planned,confirmed,completed,cancelled'
            ]);

            $data['id'] = $this->supabaseService->generateUUID();
            $data['created_by'] = Auth::id();
            
            $this->supabaseService->insert('events', $data);
            
            return redirect()->route('events.index')->with('success', 'Evento creado exitosamente');
        } catch (\Exception $e) {
            return back()->withErrors(['error' => $e->getMessage()])->withInput();
        }
    }

    public function update(Request $request, $id)
    {
        try {
            $data = $request->validate([
                'name' => 'nullable|string|max:255',
                'event_type' => 'nullable|string|in:collection,distribution,awareness,fundraising',
                'start_date' => 'nullable|date',
                'end_date' => 'nullable|date|after:start_date',
                'location' => 'nullable|string',
                'required_volunteers' => 'nullable|integer|min:1',
                'status' => 'nullable|string|in:planned,confirmed,completed,cancelled'
            ]);

            $this->supabaseService->update('events', $id, $data);
            
            return redirect()->route('events.index')->with('success', 'Evento actualizado exitosamente');
        } catch (\Exception $e) {
            return back()->withErrors(['error' => $e->getMessage()])->withInput();
        }
    }

    public function destroy($id)
    {
        try {
            $this->supabaseService->delete('events', $id);
            return redirect()->route('events.index')->with('success', 'Evento eliminado exitosamente');
        } catch (\Exception $e) {
            return back()->withErrors(['error' => $e->getMessage()]);
        }
    }
}
