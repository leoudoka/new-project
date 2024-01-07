<?php

namespace Modules\Course\app\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

use Modules\Course\Repositories\CourseRepository;
use Modules\Course\Services\CourseService;

class CourseController extends Controller
{
    /**
     * The course service
     */
    protected CourseService $courseService;

    /**
     * CourseController constructor.
     *
     * @param CourseRepository $courseRepository
     */
    public function __construct(
        CourseRepository $courseRepository
    ) {
        $this->courseService = new CourseService($courseRepository);
    }

    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return view('course::index');
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        return view('course::create');
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request): RedirectResponse
    {
        //
    }

    /**
     * Show the specified resource.
     */
    public function show($id)
    {
        return view('course::show');
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit($id)
    {
        return view('course::edit');
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, $id): RedirectResponse
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy($id)
    {
        //
    }
}
