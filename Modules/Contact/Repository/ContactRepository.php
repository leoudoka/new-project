<?php

namespace Modules\Contact\Repositories;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Auth\Events\Registered;
use Illuminate\Support\Str;

use Modules\Contact\app\Models\Contact;

class ContactRepository {

    /**
     * Get all user
     *
     * @return Contact
     */
	public function getContacts(): Collection
    {
        return Contact::all();
    }


    /**
     * Get specific contact details
     *
     * @return Contact
     */
    public static function getContactById(string $id)
    {
        return Contact::find($id);
    }
}
