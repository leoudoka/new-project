<?php

namespace Modules\Blog\Services;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

use Modules\Blog\Repositories\BlogRepository;
use Modules\Blog\app\Models\Blog;

class BlogService {

    /**
     * The blog repository
     */
    protected BlogRepository $blogRepository;

    public function __construct(
        BlogRepository $blogRepository
    )
    {
        $this->blogRepository = $blogRepository;
    }
}