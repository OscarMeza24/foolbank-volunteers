@extends('layouts.app')

@section('content')
<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Editar Evento</h1>

    <form action="{{ route('events.update', $event->id) }}" method="POST" class="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow">
        @csrf
        @method('PUT')

        <div class="mb-4">
            <label for="name" class="block text-sm font-medium text-gray-700">Nombre</label>
            <input type="text" name="name" id="name" value="{{ $event->name }}" required 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div class="mb-4">
            <label for="event_type" class="block text-sm font-medium text-gray-700">Tipo de Evento</label>
            <select name="event_type" id="event_type" required 
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                <option value="collection" {{ $event->event_type === 'collection' ? 'selected' : '' }}>Colección</option>
                <option value="distribution" {{ $event->event_type === 'distribution' ? 'selected' : '' }}>Distribución</option>
                <option value="awareness" {{ $event->event_type === 'awareness' ? 'selected' : '' }}>Concienciación</option>
                <option value="fundraising" {{ $event->event_type === 'fundraising' ? 'selected' : '' }}>Recaudación de Fondos</option>
            </select>
        </div>

        <div class="mb-4">
            <label for="start_date" class="block text-sm font-medium text-gray-700">Fecha de Inicio</label>
            <input type="date" name="start_date" id="start_date" value="{{ $event->start_date }}" required 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div class="mb-4">
            <label for="end_date" class="block text-sm font-medium text-gray-700">Fecha de Fin</label>
            <input type="date" name="end_date" id="end_date" value="{{ $event->end_date }}" required 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div class="mb-4">
            <label for="location" class="block text-sm font-medium text-gray-700">Ubicación</label>
            <input type="text" name="location" id="location" value="{{ $event->location }}" required 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div class="mb-4">
            <label for="required_volunteers" class="block text-sm font-medium text-gray-700">Voluntarios Necesarios</label>
            <input type="number" name="required_volunteers" id="required_volunteers" value="{{ $event->required_volunteers }}" required min="1" 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div class="mb-4">
            <label for="status" class="block text-sm font-medium text-gray-700">Estado</label>
            <select name="status" id="status" required 
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                <option value="planned" {{ $event->status === 'planned' ? 'selected' : '' }}>Planificado</option>
                <option value="confirmed" {{ $event->status === 'confirmed' ? 'selected' : '' }}>Confirmado</option>
                <option value="completed" {{ $event->status === 'completed' ? 'selected' : '' }}>Completado</option>
                <option value="cancelled" {{ $event->status === 'cancelled' ? 'selected' : '' }}>Cancelado</option>
            </select>
        </div>

        <div class="flex justify-end">
            <a href="{{ route('events.index') }}" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded mr-4">
                Cancelar
            </a>
            <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Guardar Cambios
            </button>
        </div>
    </form>
</div>
@endsection
