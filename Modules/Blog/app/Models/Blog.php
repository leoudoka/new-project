<?php

namespace Modules\Blog\app\Models;

use App\Models\BaseModel;

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
    protected $fillable = [];
}
