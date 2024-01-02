<?php

namespace Modules\Employer\app\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Modules\Employer\Database\factories\EmployerFactory;

class Employer extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [];
    
    protected static function newFactory(): EmployerFactory
    {
        //return EmployerFactory::new();
    }
}
