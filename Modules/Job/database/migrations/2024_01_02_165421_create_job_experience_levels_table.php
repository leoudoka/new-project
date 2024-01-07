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
            $table->enum('status', [0, 1])->default(1);
            $table->foreign('created_by')->references('id')->on('users');
            $table->timestamps();
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
