<?php

namespace Modules\Employer\Repositories;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Str;

use Modules\Employer\app\Models\Employer;

class EmployerRepository {

    /**
     * Get all employers
     *
     * @return Employer
     */
	public function getEmployers(): Collection
    {
        return Employer::all();
    }


    /**
     * Get specific employer
     *
     * @return Employer
     */
    public static function getEmployerById(string $id)
    {
        return Employer::find($id);
    }

    /**
     * Returns employer by email.
     *
     * @param $email
     *
     * @return mixed
     */
    public static function getEmployerByEmail($email)
    {
        return Employer::where(['email' => $email])->first();
    }
}
