<?php

namespace Modules\Job\app\Models;

use App\Models\BaseModel;

class JobType extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'job_types';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [];
}
