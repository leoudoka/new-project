<?php

namespace Modules\Job\app\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

use Modules\Job\Repositories\JobRepository;
use Modules\Job\Services\JobService;

class JobController extends Controller
{
    /**
     * The job service
     */
    protected JobService $jobService;

    /**
     * JobController constructor.
     *
     * @param JobRepository $jobRepository
     */
    public function __construct(
        JobRepository $jobRepository
    ) {
        $this->jobService = new JobService($jobRepository);
    }

    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return view('job::index');
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        return view('job::create');
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
        return view('job::show');
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit($id)
    {
        return view('job::edit');
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
