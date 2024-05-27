<?php

namespace Modules\Blog\app\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;

use App\Models\BaseModel;
use App\Models\User;

class Blog extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'blogs';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'title',
        'slug',
        'description',
        'status',
        'created_by'
    ];

    /**
     * Interact with the job category status.
     */
    protected function status(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => \ActiveStatus::getValue($value),
            set: fn ($value) => \ActiveStatus::setValue($value),
        );
    }

    /**
     * Interact with the blog's slug.
     */
    protected function slug(): Attribute
    {
        return Attribute::make(
            set: fn ($value) => \slugify($this, $value),
        );
    }

    /**
     * Interact with the blog createdBy.
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
