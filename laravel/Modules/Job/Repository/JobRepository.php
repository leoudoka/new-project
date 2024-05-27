<?php

namespace Modules\Job\Repositories;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Auth\Events\Registered;
use Illuminate\Support\Str;

use Modules\Job\app\Models\Job;

class JobRepository {

    /**
     * Get all job
     *
     * @return Job
     */
	public function getJobs(): Collection
    {
        return Job::all();
    }


    /**
     * Get specific job
     *
     * @return Job
     */
    public static function getJobById(string $id)
    {
        return Job::find($id);
    }
}
