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
        Schema::create('job_experience_levels', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->enum('level', [
                \JobExperienceLevelType::ANY_YEARS_OF_EXPERIENCE,
                \JobExperienceLevelType::NO_EXPERIENCE,
                \JobExperienceLevelType::INTERNSHIP_GRADUATE,
                \JobExperienceLevelType::ENTRY_LEVEL,
                \JobExperienceLevelType::MID_LEVEL,
                \JobExperienceLevelType::SENIOR_LEVEL,
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
        Schema::dropIfExists('job_experience_levels');
    }
};
