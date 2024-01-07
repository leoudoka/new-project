<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

use App\Models\User;
use App\Models\Address;

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
            $table->foreignIdFor(User::class);
            $table->enum('status', [0, 1])->default(1);
            $table->timestamps();
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
