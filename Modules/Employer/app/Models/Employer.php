<?php

namespace Modules\Employer\app\Models;

use App\Models\BaseModel;

class Employer extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'employers';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [];
}
