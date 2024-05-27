<?php

namespace Modules\Admin\Services;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

use Modules\Admin\Repositories\AdminRepository;

class AdminService {

    /**
     * The admin repository
     */
    protected AdminRepository $adminRepository;

    public function __construct(
        AdminRepository $adminRepository
    )
    {
        $this->adminRepository = $adminRepository;
    }
}