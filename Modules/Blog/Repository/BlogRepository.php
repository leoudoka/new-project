<?php

namespace Modules\Blog\Repositories;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Auth\Events\Registered;
use Illuminate\Support\Str;

use Modules\Blog\app\Models\Blog;

class BlogRepository {

    /**
     * Get all blog
     *
     * @return Blog
     */
	public function getBlogs(): Collection
    {
        return Blog::all();
    }


    /**
     * Get specific blog
     *
     * @return Blog
     */
    public static function getBlogById(string $id)
    {
        return Blog::find($id);
    }
}
