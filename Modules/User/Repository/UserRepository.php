<?php

namespace Modules\User\Repositories;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Auth\Events\Registered;
use Illuminate\Support\Str;

use App\Models\User;

class UserRepository {

    /**
     * Get all user
     *
     * @return User
     */
	public function getUsers(): Collection
    {
        return User::all();
    }


    /**
     * Get specific user
     *
     * @return User
     */
    public static function getUserById(string $id)
    {
        return User::find($id);
    }

    /**
     * Returns user by email.
     *
     * @param $email
     *
     * @return mixed
     */
    public static function getUserByEmail($email)
    {
        return User::where(['email' => $email])->first();
    }
}
