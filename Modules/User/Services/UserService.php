<?php

namespace Modules\User\Services;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

use Modules\User\Repositories\UserRepository;
use App\Models\User;

class UserService {

    /**
     * The User repository
     */
    protected UserRepository $userRepository;

    public function __construct(
        UserRepository $userRepository
    )
    {
        $this->userRepository = $userRepository;
    }
}