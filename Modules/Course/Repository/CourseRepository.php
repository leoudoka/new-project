<?php

namespace Modules\Course\Repositories;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Auth\Events\Registered;
use Illuminate\Support\Str;

use Modules\Course\app\Models\Course;

class CourseRepository {

    /**
     * Get all course
     *
     * @return Course
     */
	public function getCourses(): Collection
    {
        return Course::all();
    }


    /**
     * Get specific course
     *
     * @return Course
     */
    public static function getCourseById(string $id)
    {
        return Course::find($id);
    }
}
