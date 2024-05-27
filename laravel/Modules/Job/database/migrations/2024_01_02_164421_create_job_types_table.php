<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('job_types', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->enum('type', [
                \JobTypeK::CONTRACT,
                \JobTypeK::FULL_GRADUATE,
                \JobTypeK::INTERNSHIP_GRADUATE,
                \JobTypeK::PART_TIME
            ])->unique();
            $table->string('description')->nullable();
            $table->enum('status', [
                \ActiveStatus::INACTIVE,
                \ActiveStatus::ACTIVE
            ])->default(\ActiveStatus::ACTIVE);
            $table->bigInteger('created_by')->nullable();
            $table->timestamps();
            $table->foreign('created_by')->references('id')->on('users')->onDelete('SET NULL');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('job_types');
    }
};
