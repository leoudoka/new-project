<?php

namespace Modules\Contact\app\Models;

use App\Models\BaseModel;

class Contact extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'contact_us';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'name',
        'email',
        'message',
        'mobile_number'
    ];

}
