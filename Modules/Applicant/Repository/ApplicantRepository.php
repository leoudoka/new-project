<?php

namespace Modules\Applicant\Repositories;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Auth\Events\Registered;
use Illuminate\Support\Str;

use Modules\Applicant\app\Models\Applicant;

class ApplicantRepository {

    /**
     * Get all applicant
     *
     * @return Applicant
     */
	public function getApplicants(): Collection
    {
        return Applicant::all();
    }


    /**
     * Get specific applicant
     *
     * @return Applicant
     */
    public static function getApplicantById(string $id)
    {
        return Applicant::find($id);
    }

    /**
     * Returns applicant by email.
     *
     * @param $email
     *
     * @return mixed
     */
    public static function getApplicantByEmail($email)
    {
        return Applicant::where(['email' => $email])->first();
    }
}
