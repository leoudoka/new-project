<?php

namespace Modules\Applicant\app\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Modules\Applicant\Database\factories\ApplicantFactory;

class Applicant extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [];
    
    protected static function newFactory(): ApplicantFactory
    {
        //return ApplicantFactory::new();
    }
}
