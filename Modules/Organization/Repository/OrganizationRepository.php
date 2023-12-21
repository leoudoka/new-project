<?php

namespace Modules\Organization\Repositories;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Auth\Events\Registered;
use Illuminate\Support\Str;

use Modules\Organization\app\Models\Organization;

class OrganizationRepository {

    /**
     * Get all org.
     *
     * @return Organization
     */
	public function getOrganizations(): Collection
    {
        return Organization::all();
    }


    /**
     * Get specific org.
     *
     * @return Organization
     */
    public static function getOrganizationById(string $id)
    {
        return Organization::find($id);
    }
}
