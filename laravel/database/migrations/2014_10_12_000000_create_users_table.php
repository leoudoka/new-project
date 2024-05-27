<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

use App\Models\Attachment;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('users', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('first_name', 30)->nullable();
            $table->string('middle_name', 30)->nullable();
            $table->string('last_name', 30)->nullable();
            $table->string('email')->unique();
            $table->string('mobile_number', 15)->nullable();
            $table->enum('gender', [
                \Gender::MALE, 
                \Gender::FEMALE, 
                \Gender::NOT_SPECIFIED
            ])->nullable();
            $table->timestamp('email_verified_at')->nullable();
            $table->date('dob')->nullable();
            $table->string('password');
            $table->enum('is_active', [
                \ActiveStatus::INACTIVE,
                \ActiveStatus::ACTIVE, 
            ])->default(\ActiveStatus::ACTIVE);
            $table->foreignIdFor(Attachment::class)->nullable();
            $table->rememberToken();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('users');
    }
};
