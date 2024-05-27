<?php

namespace Modules\Job\app\Models;

use Illuminate\Database\Eloquent\Relations\HasOne;

use App\Models\BaseModel;
use App\Models\User;
use Modules\Employer\app\Models\Employer;

class Job extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'jobs';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'job_category_id',
        'job_industries_id',
        'job_experirnce_level_id',
        'job_type_id',
        'country_id',
        'state_id',
        'summary',
        'description',
        'remuneration',
        'featured',
        'status',
        'created_by'
    ];

    /**
     * Get the employer associated with the job.
     */
    public function employer(): HasOne
    {
        return $this->hasOne(Employer::class);
    }

    /**
     * Interact with the job's createdBy.
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
