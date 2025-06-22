<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Volunteer extends Model
{
    protected $fillable = [
        'user_id',
        'skills',
        'availability',
        'has_transport',
        'reliability_score',
        'total_hours_volunteered'
    ];

    protected $casts = [
        'skills' => 'array',
        'availability' => 'array',
        'has_transport' => 'boolean',
        'reliability_score' => 'decimal:2',
        'total_hours_volunteered' => 'integer'
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function assignments(): HasMany
    {
        return $this->hasMany(Assignment::class);
    }

    public function events()
    {
        return $this->belongsToMany(Event::class, 'assignments')
            ->withPivot('role', 'status', 'assigned_by')
            ->withTimestamps();
    }

    public function calculateMatchScore(Event $event): float
    {
        $score = 0;
        
        // Matching de habilidades (50% del score)
        if ($event->skills_required && $this->skills) {
            $commonSkills = array_intersect($event->skills_required, $this->skills);
            $score += 0.5 * (count($commonSkills) / count($event->skills_required));
        }
        
        // Score de confiabilidad (20%)
        $score += 0.2 * $this->reliability_score;
        
        // Experiencia previa (15%)
        $score += 0.15 * min(1, $this->total_hours_volunteered / 100);
        
        // Transporte (15%)
        if ($event->event_type === 'distribution' && $this->has_transport) {
            $score += 0.15;
        }
        
        return min(1, $score);
    }
}
