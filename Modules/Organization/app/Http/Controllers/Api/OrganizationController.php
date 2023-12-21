<?php

namespace Modules\Organization\app\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

use Modules\Organization\Repositories\OrganizationRepository;
use Modules\Organization\Services\OrganizationService;

class OrganizationController extends Controller
{
    /**
     * The organization service
     */
    protected OrganizationService $organizationService;

    /**
     * OrganizationController constructor.
     *
     * @param OrganizationRepository $organizationRepository
     */
    public function __construct(
        OrganizationRepository $organizationRepository
    ) {
        $this->organizationService = new OrganizationService($organizationRepository);
    }

    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return view('organization::index');
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        return view('organization::create');
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
        return view('organization::show');
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit($id)
    {
        return view('organization::edit');
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
