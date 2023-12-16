<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

use App\Models\User;

class SuperAdminSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // create super-admin user
        $user = User::create([
            'first_name' => 'Super',
            'last_name' => 'Admin',
            'email' => env('SUPER_ADMIN_EMAIL'),
            'password' => Hash::make(env('SUPER_ADMIN_PASSWORD')),
            'email_verified_at' => now(),
            'is_active' => \ActiveStatus::ACTIVE,
            'remember_token' => Str::random(10),
        ]);
    }
}
