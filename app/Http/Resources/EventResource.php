<?php

namespace App\Http\Resources;

use App\Http\Resources\VolunteerResource;
use Illuminate\Http\Resources\Json\JsonResource;

class EventResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'description' => $this->description,
            'date' => $this->date,
            'location' => $this->location,
            'required_volunteers' => $this->required_volunteers,
            'skills_required' => $this->skills_required,
            'volunteers' => VolunteerResource::collection($this->whenLoaded('volunteers')),
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
