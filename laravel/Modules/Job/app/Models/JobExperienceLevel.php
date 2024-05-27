<?php

namespace Modules\Job\app\Models;

use App\Models\BaseModel;
use App\Models\User;

class JobExperienceLevel extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'job_experience_levels';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'level',
        'description',
        'status',
        'created_by'
    ];

    /**
     * Interact with the job experience level status.
     */
    protected function status(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => \ActiveStatus::getValue($value),
            set: fn ($value) => \ActiveStatus::setValue($value),
        );
    }

    /**
     * Interact with the job experience level createdBy.
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
