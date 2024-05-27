<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

/**
 * App\Models\BaseModel
 *
 * @property-read mixed $create_at
 * @property-read mixed $updated_at
 * @mixin \Eloquent
 */
class BaseModel extends Model
{
    use HasFactory;

     /**
     * Indicates if the model should be timestamped.
     *
     * @var bool
     */
    public $timestamps = true;

}
