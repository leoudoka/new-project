<?php

namespace Modules\Contact\Services;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

use Modules\Contact\Repositories\ContactRepository;

class ContactService {

    /**
     * The contact repository
     */
    protected ContactRepository $contactRepository;

    public function __construct(
        ContactRepository $contactRepository
    )
    {
        $this->contactRepository = $contactRepository;
    }
}