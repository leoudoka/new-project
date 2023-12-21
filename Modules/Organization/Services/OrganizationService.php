<?php

namespace Modules\Organization\Services;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

use Modules\Organization\Repositories\UserRepository;
use Modules\Organization\app\Models\Organization;

class OrganizationService {

    /**
     * The organization repository
     */
    protected OrganizationRepository $organizationRepository;

    public function __construct(
        OrganizationRepository $organizationRepository
    )
    {
        $this->organizationRepository = $organizationRepository;
    }
}