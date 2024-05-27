<?php

namespace Modules\Job\Services;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

use Modules\Job\Repositories\JobRepository;
use Modules\Job\app\Models\Job;

class JobService {

    /**
     * The job repository
     */
    protected JobRepository $jobRepository;

    public function __construct(
        JobRepository $jobRepository
    )
    {
        $this->jobRepository = $jobRepository;
    }
}