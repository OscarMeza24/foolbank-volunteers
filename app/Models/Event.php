<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Event extends Model
{
    protected $fillable = [
        'name',
        'description',
        'event_type',
        'start_date',
        'end_date',
        'location',
        'latitude',
        'longitude',
        'required_volunteers',
        'skills_required',
        'status',
        'created_by'
    ];

    protected $casts = [
        'start_date' => 'datetime',
        'end_date' => 'datetime',
        'skills_required' => 'array',
        'latitude' => 'decimal:8',
        'longitude' => 'decimal:8'
    ];

    public function assignments(): HasMany
    {
        return $this->hasMany(Assignment::class);
    }

    public function volunteers()
    {
        return $this->belongsToMany(Volunteer::class, 'assignments')
            ->withPivot('role', 'status', 'assigned_by')
            ->withTimestamps();
    }

    public function creator()
    {
        return $this->belongsTo(User::class, 'created_by');
    }

    public function isFullyStaffed(): bool
    {
        return $this->volunteers()->wherePivot('status', 'assigned')->count() >= $this->required_volunteers;
    }
}
