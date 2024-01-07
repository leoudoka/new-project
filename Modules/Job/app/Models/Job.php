<?php

namespace Modules\Job\app\Models;

use App\Models\BaseModel;

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
    protected $fillable = [];
}
