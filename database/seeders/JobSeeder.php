<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

use Modules\Job\app\Models\JobCategory;
use Modules\Job\app\Models\JobType;
use Modules\Job\app\Models\JobExperienceLevel;

class JobSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // create the default experience level (5)
        for ($i=0; $i < 5; $i++) { 
            JobType::create([
                'type' => \JobTypeK::setAll()[$i]
            ]);
        }

        // create the default experience level (6)
        for ($i=0; $i < 7; $i++) { 
            JobExperienceLevel::create([
                'level' => \JobExperienceLevelType::setAll()[$i]
            ]);
        }
    }
}
