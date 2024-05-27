<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

use App\Models\Address;
use App\Models\Attachment;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('employers', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('name', 50);
            $table->string('slug', 70)->unique();
            $table->text('about')->nullable();
            $table->foreignId('country_id', 10)->nullable();
            $table->foreignId('state_id', 10)->nullable();
            $table->foreignIdFor(Address::class)->nullable();
            $table->foreignIdFor(Attachment::class)->nullable();
            $table->enum('status', [0, 1])->default(1);
            $table->enum('is_approved', [
                \ActiveStatus::INACTIVE,
                \ActiveStatus::ACTIVE, 
            ])->default(\ActiveStatus::INACTIVE);
            $table->bigInteger('approved_by')->nullable();
            $table->bigInteger('created_by')->nullable();
            $table->timestamps();
            $table->foreign('approved_by')->references('id')->on('users')->onDelete('SET NULL');
            $table->foreign('created_by')->references('id')->on('users')->onDelete('SET NULL');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('employers');
    }
};
