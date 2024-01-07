<?php

namespace Modules\Course\app\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;

use App\Models\BaseModel;
use App\Models\User;

class Course extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'courses';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'title',
        'slug',
        'description',
        'attachment_id',
        'course_category_id',
        'status',
        'created_by'
    ];

    /**
     * Interact with the course's slug.
     */
    protected function slug(): Attribute
    {
        return Attribute::make(
            set: fn ($value) => \slugify($this, $value),
        );
    }

    /**
     * Interact with the course createdBy.
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
