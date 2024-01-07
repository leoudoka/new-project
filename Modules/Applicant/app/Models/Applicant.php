<?php

namespace Modules\Applicant\app\Models;

use App\Models\BaseModel;

class Applicant extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'applicants';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [];
}
