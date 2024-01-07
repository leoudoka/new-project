<?php

namespace Modules\Job\app\Models;

use App\Models\BaseModel;

class JobIndustry extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'job_industries';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [];
}
