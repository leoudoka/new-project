<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

use Modules\Job\app\Models\JobCategory;
use Modules\Job\app\Models\JobIndustry;
use Modules\Job\app\Models\JobExperienceLevel;
use Modules\Job\app\Models\JobType;
use Modules\Employer\app\Models\Employer;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('jobs', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('title');
            $table->foreignIdFor(JobCategory::class);
            $table->foreignIdFor(JobIndustry::class)->nullable();
            $table->foreignIdFor(JobExperienceLevel::class)->default(\JobExperienceLevelType::ANY_YEARS_OF_EXPERIENCE);
            $table->foreignIdFor(JobType::class)->nullable();
            $table->foreignId('country_id', 10)->nullable();
            $table->foreignId('state_id', 10)->nullable();
            $table->text('summary')->nullable();
            $table->longText('description');
            $table->string('remuneration')->nullable();
            $table->enum('featured', [0, 1])->default(0);
            $table->enum('status', [
                \JobStatus::NEW,
                \JobStatus::OPEN,
                \JobStatus::CLOSED
            ])->default(\JobStatus::NEW);
            $table->foreignIdFor(Employer::class);
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
        Schema::dropIfExists('jobs');
    }
};
