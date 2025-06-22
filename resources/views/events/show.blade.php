@extends('layouts.app')

@section('content')
<div class="container mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow p-6">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold">{{ $event->name }}</h1>
            <div class="flex space-x-4">
                <a href="{{ route('events.edit', $event->id) }}" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Editar Evento
                </a>
                <form action="{{ route('events.destroy', $event->id) }}" method="POST" class="inline">
                    @csrf
                    @method('DELETE')
                    <button type="submit" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded" onclick="return confirm('¿Estás seguro de eliminar este evento?')">
                        Eliminar Evento
                    </button>
                </form>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <h2 class="text-xl font-semibold mb-4">Información Básica</h2>
                <div class="space-y-4">
                    <div>
                        <span class="font-medium text-gray-600">Tipo de Evento:</span>
                        <span class="ml-2">{{ $event->event_type }}</span>
                    </div>
                    <div>
                        <span class="font-medium text-gray-600">Fecha:</span>
                        <span class="ml-2">{{ $event->start_date }} - {{ $event->end_date }}</span>
                    </div>
                    <div>
                        <span class="font-medium text-gray-600">Ubicación:</span>
                        <span class="ml-2">{{ $event->location }}</span>
                    </div>
                    <div>
                        <span class="font-medium text-gray-600">Voluntarios Necesarios:</span>
                        <span class="ml-2">{{ $event->required_volunteers }}</span>
                    </div>
                    <div>
                        <span class="font-medium text-gray-600">Estado:</span>
                        <span class="ml-2 {{ $event->status === 'completed' ? 'text-green-600' : ($event->status === 'cancelled' ? 'text-red-600' : 'text-blue-600') }}">
                            {{ $event->status }}
                        </span>
                    </div>
                </div>
            </div>

            <div>
                <h2 class="text-xl font-semibold mb-4">Ubicación</h2>
                <div class="bg-gray-50 p-4 rounded">
                    <div id="map" style="height: 300px;"></div>
                </div>
            </div>
        </div>
    </div>
</div>

@push('scripts')
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY"></script>
<script>
    function initMap() {
        const map = new google.maps.Map(document.getElementById('map'), {
            zoom: 15,
            center: { lat: {{ $event->latitude ?? 0 }}, lng: {{ $event->longitude ?? 0 }} }
        });

        const marker = new google.maps.Marker({
            position: { lat: {{ $event->latitude ?? 0 }}, lng: {{ $event->longitude ?? 0 }} },
            map: map,
            title: '{{ $event->name }}'
        });
    }

    // Initialize the map when the page loads
    window.addEventListener('load', initMap);
</script>
@endpush
@endsection
