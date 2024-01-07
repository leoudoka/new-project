<?php

namespace Modules\Course\app\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;

use App\Models\BaseModel;
use App\Models\User;

class CourseCategories extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'course_categories';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'name',
        'slug',
        'description',
        'created_by'
    ];
    
    /**
     * Interact with the course category slug.
     */
    protected function slug(): Attribute
    {
        return Attribute::make(
            set: fn ($value) => \slugify($this, $value),
        );
    }

    /**
     * Interact with the course category createdBy.
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
