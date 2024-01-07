<?php

namespace Modules\Course\app\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;

use App\Models\BaseModel;
use App\Models\User;

class Lesson extends BaseModel
{
     /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'lessons';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'lesson_number',
        'lesson_type',
        'title',
        'article',
        'external_url',
        'attachment_id',
        'course_section_id',
        'created_by'
    ];

    /**
     * Interact with the lesson createdBy.
     */
    protected function createdBy(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => User::selectRaw(
                                    'CONCAT(first_name, " ", last_name) as created_by'
                                )
                                ->where('id', $value)
                                ->first()
        );
    }
}
