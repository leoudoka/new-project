<?php

namespace Modules\Employer\Services;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

use Modules\Employer\Repositories\EmployerRepository;

class EmployerService {

    /**
     * The employer repository
     */
    protected EmployerRepository $employerRepository;

    public function __construct(
        EmployerRepository $employerRepository
    )
    {
        $this->employerRepository = $employerRepository;
    }
}