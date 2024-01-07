<?php

namespace Modules\Job\app\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Modules\Job\Database\factories\JobFactory;

class Job extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [];
    
    protected static function newFactory(): JobFactory
    {
        //return JobFactory::new();
    }
}
