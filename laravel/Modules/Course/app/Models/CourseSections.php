<?php

namespace Modules\Course\app\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;

use App\Models\BaseModel;
use App\Models\User;

class CourseSections extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'course_sections';
    
    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'title',
        'section_number',
        'course_id',
        'created_by'
    ];

    /**
     * Interact with the course section createdBy.
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
