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
        Schema::create('attachments', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('name', 100);
            $table->string('path', 255);
            $table->bigInteger('entity_id');
            $table->enum('entity_type', [
                \EntityType::USER_PROFILE_IMAGE,
                \EntityType::COURSE_COVER_IMAGE,
                \EntityType::LESSON_VIDEO,
                \EntityType::EMPLOYER_COMPANY_LOGO,
                \EntityType::APPLICANT_CV,
                \EntityType::APPLICANT_COVER_LETTER,
            ]);
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
        Schema::dropIfExists('attachments');
    }
};
