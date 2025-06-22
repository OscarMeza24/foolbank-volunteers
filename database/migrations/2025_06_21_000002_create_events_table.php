<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('events', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->text('description')->nullable();
            $table->enum('event_type', ['collection', 'distribution', 'awareness', 'fundraising']);
            $table->timestamp('start_date');
            $table->timestamp('end_date');
            $table->text('location');
            $table->decimal('latitude', 10, 8)->nullable();
            $table->decimal('longitude', 10, 8)->nullable();
            $table->integer('required_volunteers');
            $table->json('skills_required')->nullable();
            $table->enum('status', ['planned', 'confirmed', 'completed', 'cancelled'])->default('planned');
            $table->foreignId('created_by')->constrained()->onDelete('cascade');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('events');
    }
};
