<?php

namespace App\Models;

class Address extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'addresses';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'address',
        'city_id',
        'country_id',
        'postal_code',
        'user_id'
    ];
}
