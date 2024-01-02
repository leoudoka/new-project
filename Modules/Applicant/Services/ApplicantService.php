<?php

namespace Modules\Applicant\Services;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

use Modules\Applicant\Repositories\ApplicantRepository;

class ApplicantService {

    /**
     * The applicant repository
     */
    protected ApplicantRepository $applicantRepository;

    public function __construct(
        ApplicantRepository $applicantRepository
    )
    {
        $this->applicantRepository = $applicantRepository;
    }
}