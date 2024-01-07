<?php

namespace Modules\Course\app\Models;

use App\Models\BaseModel;

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
    protected $fillable = [];
}
