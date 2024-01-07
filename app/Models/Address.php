<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;

use App\Models\BaseModel;

class Address extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'address';

    protected $fillable = [
        'address',
        'city_id',
        'country_id',
        'postal_code',
        'user_id'
    ];
}
