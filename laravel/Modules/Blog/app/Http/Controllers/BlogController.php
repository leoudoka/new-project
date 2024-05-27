<?php

namespace Modules\Blog\app\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

use Modules\Blog\Repositories\BlogRepository;
use Modules\Blog\Services\BlogService;

class BlogController extends Controller
{
    /**
     * The blog service
     */
    protected BlogService $blogService;

    /**
     * BlogController constructor.
     *
     * @param BlogRepository $blogRepository
     */
    public function __construct(
        BlogRepository $blogRepository
    ) {
        $this->blogService = new BlogService($blogRepository);
    }

    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return view('blog::index');
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        return view('blog::create');
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
        return view('blog::show');
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit($id)
    {
        return view('blog::edit');
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
