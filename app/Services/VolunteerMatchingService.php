<?php

namespace App\Services;

use App\Models\Event;
use App\Models\Volunteer;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

class VolunteerMatchingService
{
    protected $cachePrefix = 'volunteer_match_';
    protected $cacheDuration = 60; // 1 hour

    public function matchVolunteersToEvent(Event $event): Collection
    {
        try {
            // Intentar obtener de cache
            $cacheKey = $this->cachePrefix . 'event_' . $event->id;
            $matches = Cache::get($cacheKey);

            if ($matches) {
                return collect($matches);
            }

            // 1. Obtener voluntarios disponibles
            $volunteers = Volunteer::with('user')
                ->whereNotIn('id', function ($query) use ($event) {
                    $query->select('volunteer_id')
                        ->from('assignments')
                        ->where('event_id', $event->id)
                        ->where('status', 'assigned');
                })
                ->where('availability', 'LIKE', '%' . $event->start_date->format('l') . '%')
                ->get();

            // 2. Calcular score de matching para cada voluntario
            $matches = $volunteers->map(function ($volunteer) use ($event) {
                $score = $this->calculateMatchScore($volunteer, $event);
                
                return [
                    'volunteer_id' => $volunteer->id,
                    'volunteer_name' => $volunteer->user->name,
                    'match_score' => $score,
                    'reason' => $this->getMatchReason($volunteer, $event, $score),
                    'skills_match' => $this->calculateSkillsMatch($volunteer, $event),
                    'availability_match' => $this->calculateAvailabilityMatch($volunteer, $event),
                    'reliability_score' => $volunteer->reliability_score,
                    'total_hours_volunteered' => $volunteer->total_hours_volunteered
                ];
            });

            // 3. Filtrar y ordenar
            $filtered = $matches->where('match_score', '>', 0.6)
                               ->sortByDesc('match_score')
                               ->take(10);

            // Guardar en cache
            Cache::put($cacheKey, $filtered->toArray(), $this->cacheDuration);

            return $filtered;
        } catch (\Exception $e) {
            Log::error('Error matching volunteers for event: ' . $e->getMessage());
            throw $e;
        }
    }

    public function findMatchingEvents(string $volunteerId, array $filters = []): Collection
    {
        try {
            // Intentar obtener de cache
            $cacheKey = $this->cachePrefix . 'volunteer_' . $volunteerId;
            $matches = Cache::get($cacheKey);

            if ($matches) {
                return collect($matches);
            }

            $events = Event::with('volunteers')
                ->where('status', 'planned')
                ->where('start_date', '>', now())
                ->when($filters['location'] ?? null, function ($query, $location) {
                    $query->where('location', 'LIKE', "%{$location}%");
                })
                ->when($filters['radius'] ?? null, function ($query, $radius) use ($filters) {
                    if ($filters['location']) {
                        $query->whereRaw("ST_DWithin(
                            ST_SetSRID(ST_Point(longitude, latitude), 4326),
                            ST_SetSRID(ST_Point(?, ?), 4326),
                            ?
                        )", [
                            $filters['longitude'],
                            $filters['latitude'],
                            $radius * 1000
                        ]);
                    }
                })
                ->get();

            $volunteer = Volunteer::with('user')->findOrFail($volunteerId);

            $matches = $events->map(function ($event) use ($volunteer) {
                $score = $this->calculateMatchScore($volunteer, $event);
                
                return [
                    'event' => $event,
                    'match_score' => $score,
                    'reason' => $this->getMatchReason($volunteer, $event, $score),
                    'distance' => $this->calculateDistance($volunteer, $event)
                ];
            })->sortByDesc('match_score');

            // Guardar en cache
            Cache::put($cacheKey, $matches->toArray(), $this->cacheDuration);

            return $matches;
        } catch (\Exception $e) {
            Log::error('Error finding matching events: ' . $e->getMessage());
            throw $e;
        }
    }

    protected function calculateMatchScore(Volunteer $volunteer, Event $event): float
    {
        $score = 0;
        
        // Matching de habilidades (50% del score)
        if ($event->skills_required && $volunteer->skills) {
            $commonSkills = array_intersect($event->skills_required, $volunteer->skills);
            $score += 0.5 * (count($commonSkills) / count($event->skills_required));
        }
        
        // Score de confiabilidad (20%)
        $score += 0.2 * $volunteer->reliability_score;
        
        // Experiencia previa (15%)
        $score += 0.15 * min(1, $volunteer->total_hours_volunteered / 100);
        
        // Disponibilidad (10%)
        $score += 0.1 * $this->calculateAvailabilityMatch($volunteer, $event);
        
        // Distancia (5%)
        if ($event->latitude && $event->longitude) {
            $score += 0.05 * (1 - $this->calculateDistance($volunteer, $event) / 100);
        }
        
        return min(1, $score);
    }

    protected function calculateSkillsMatch(Volunteer $volunteer, Event $event): float
    {
        if (!$event->skills_required || !$volunteer->skills) {
            return 0;
        }

        $commonSkills = array_intersect($event->skills_required, $volunteer->skills);
        return count($commonSkills) / count($event->skills_required);
    }

    protected function calculateAvailabilityMatch(Volunteer $volunteer, Event $event): float
    {
        if (!$volunteer->availability || !$event->start_date) {
            return 0;
        }

        $day = $event->start_date->format('l');
        return in_array($day, $volunteer->availability) ? 1 : 0;
    }

    protected function calculateDistance(Volunteer $volunteer, Event $event): float
    {
        if (!$event->latitude || !$event->longitude || !$volunteer->location) {
            return 0;
        }

        // Convertir la ubicación del voluntario a coordenadas
        $volunteerLocation = explode(',', $volunteer->location);
        if (count($volunteerLocation) !== 2) {
            return 0;
        }

        $lat1 = deg2rad($volunteerLocation[0]);
        $lon1 = deg2rad($volunteerLocation[1]);
        $lat2 = deg2rad($event->latitude);
        $lon2 = deg2rad($event->longitude);

        $R = 6371; // Radio de la Tierra en km
        $dLat = $lat2 - $lat1;
        $dLon = $lon2 - $lon1;

        $a = sin($dLat/2) * sin($dLat/2) +
             cos($lat1) * cos($lat2) *
             sin($dLon/2) * sin($dLon/2);
        $c = 2 * atan2(sqrt($a), sqrt(1-$a));
        
        return $R * $c;
    }

    protected function getMatchReason(Volunteer $volunteer, Event $event, float $score): string
    {
        $reasons = [];
        
        // Habilidades
        if ($event->skills_required && $volunteer->skills) {
            $commonSkills = array_intersect($event->skills_required, $volunteer->skills);
            if (!empty($commonSkills)) {
                $reasons[] = 'Posee habilidades requeridas: ' . implode(', ', $commonSkills);
            }
        }
        
        // Disponibilidad
        if ($volunteer->availability) {
            $day = $event->start_date->format('l');
            if (in_array($day, $volunteer->availability)) {
                $reasons[] = 'Disponible el día del evento';
            }
        }
        
        // Transporte
        if ($event->event_type === 'distribution' && $volunteer->has_transport) {
            $reasons[] = 'Tiene transporte propio para evento de distribución';
        }
        
        // Experiencia
        if ($volunteer->total_hours_volunteered > 0) {
            $reasons[] = 'Experiencia previa (' . $volunteer->total_hours_volunteered . ' horas)';
        }
        
        // Cercanía
        if ($event->latitude && $event->longitude) {
            $distance = $this->calculateDistance($volunteer, $event);
            if ($distance < 10) { // dentro de 10km
                $reasons[] = 'Ubicación cercana al evento';
            }
        }
        
        return implode(', ', $reasons) ?: 'Voluntario potencialmente adecuado';
    }
}
