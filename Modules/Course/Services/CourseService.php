<?php

namespace Modules\Course\Services;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

use Modules\Course\Repositories\CourseRepository;
use Modules\Course\app\Models\Course;

class CourseService {

    /**
     * The course repository
     */
    protected CourseRepository $courseRepository;

    public function __construct(
        CourseRepository $courseRepository
    )
    {
        $this->courseRepository = $courseRepository;
    }
}