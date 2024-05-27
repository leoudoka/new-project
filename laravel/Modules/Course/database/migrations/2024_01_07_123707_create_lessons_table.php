<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

use Modules\Course\app\Models\CourseSections;
use App\Models\Attachment;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('lessons', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->tinyInteger('lesson_number');
            $table->enum('lesson_type', [\LessonTypes::VIDEO, \LessonTypes::ARTICLE]);
            $table->text('title', 255);
            $table->longText('article')->nullable();
            $table->string('external_url')->nullable();
            $table->foreignIdFor(Attachment::class)->nullable();
            $table->foreignIdFor(CourseSections::class);
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
        Schema::dropIfExists('lessons');
    }
};
