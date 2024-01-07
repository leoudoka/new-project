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
        Schema::create('job_categories', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('name', 100);
            $table->string('slug', 120)->unique();
            $table->string('description')->nullable();
            $table->enum('status', [
                \ActiveStatus::INACTIVE,
                \ActiveStatus::ACTIVE
            ])->default(\ActiveStatus::ACTIVE);
            $table->bigInteger('created_by')->nullable();
            $table->timestamps();
            $table->foreign('created_by')->references('id')->on('users')->onDelete('SET NULL');
        });

        Schema::create('job_industries', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('name', 100);
            $table->string('slug', 120)->unique();
            $table->string('description')->nullable();
            $table->enum('status', [0, 1])->default(1);
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
        Schema::dropIfExists('job_categories');
        Schema::dropIfExists('job_industries');
    }
};
