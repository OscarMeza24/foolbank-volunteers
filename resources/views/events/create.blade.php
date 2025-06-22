@extends('layouts.app')

@section('content')
<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Crear Nuevo Evento</h1>

    <form action="{{ route('events.store') }}" method="POST" class="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow">
        @csrf

        <div class="mb-4">
            <label for="name" class="block text-sm font-medium text-gray-700">Nombre</label>
            <input type="text" name="name" id="name" required 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div class="mb-4">
            <label for="event_type" class="block text-sm font-medium text-gray-700">Tipo de Evento</label>
            <select name="event_type" id="event_type" required 
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                <option value="collection">Colección</option>
                <option value="distribution">Distribución</option>
                <option value="awareness">Concienciación</option>
                <option value="fundraising">Recaudación de Fondos</option>
            </select>
        </div>

        <div class="mb-4">
            <label for="start_date" class="block text-sm font-medium text-gray-700">Fecha de Inicio</label>
            <input type="date" name="start_date" id="start_date" required 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div class="mb-4">
            <label for="end_date" class="block text-sm font-medium text-gray-700">Fecha de Fin</label>
            <input type="date" name="end_date" id="end_date" required 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div class="mb-4">
            <label for="location" class="block text-sm font-medium text-gray-700">Ubicación</label>
            <input type="text" name="location" id="location" required 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div class="mb-4">
            <label for="required_volunteers" class="block text-sm font-medium text-gray-700">Voluntarios Necesarios</label>
            <input type="number" name="required_volunteers" id="required_volunteers" required min="1" 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div class="mb-4">
            <label for="status" class="block text-sm font-medium text-gray-700">Estado</label>
            <select name="status" id="status" required 
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                <option value="planned">Planificado</option>
                <option value="confirmed">Confirmado</option>
                <option value="completed">Completado</option>
                <option value="cancelled">Cancelado</option>
            </select>
        </div>

        <div class="flex justify-end">
            <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Crear Evento
            </button>
        </div>
    </form>
</div>
@endsection
