<?php

namespace Modules\Job\app\Models;

use App\Models\BaseModel;

class JobCategory extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'job_categories';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [];
}
