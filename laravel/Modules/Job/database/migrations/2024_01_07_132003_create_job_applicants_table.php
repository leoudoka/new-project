<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

use Modules\Job\app\Models\Job;
use Modules\Employer\app\Models\Employer;
use App\Models\User;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('job_applicants', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->foreignIdFor(Job::class)->nullable();
            $table->foreignIdFor(Employer::class)->nullable();
            $table->foreignIdFor(User::class)->nullable();
            $table->bigInteger('cover_letter_attachment_id')->nullable();
            $table->bigInteger('cv_attachment_id')->nullable();
            $table->enum('status', [
                \VettingStatus::ACCEPTED,
                \VettingStatus::PENDING,
                \VettingStatus::REJECTED
            ])->default(\VettingStatus::PENDING);
            $table->enum('is_approved', [
                \ActiveStatus::INACTIVE,
                \ActiveStatus::ACTIVE, 
            ])->default(\ActiveStatus::INACTIVE);
            $table->bigInteger('vetted_by')->nullable();
            $table->bigInteger('approved_by')->nullable();
            $table->timestamps();
            $table->foreign('cover_letter_attachment_id')->references('id')->on('attachments')->onDelete('SET NULL');
            $table->foreign('cv_attachment_id')->references('id')->on('attachments')->onDelete('SET NULL');
            $table->foreign('vetted_by')->references('id')->on('users')->onDelete('SET NULL');
            $table->foreign('approved_by')->references('id')->on('users')->onDelete('SET NULL');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('job_applicants');
    }
};
