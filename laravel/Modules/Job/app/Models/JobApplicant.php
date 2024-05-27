<?php

namespace Modules\Job\app\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

use App\Models\BaseModel;
use App\Models\User;
use Modules\Employer\app\Models\Employer;
use Modules\Job\app\Models\Job;


class JobApplicant extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'job_applicants';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'job_id',
        'employer_id',
        'user_id',
        'cover_letter_attachment_id',
        'cv_attachment_id',
        'status',
        'is_approved',
        'approved_by',
        'vetted_by',
    ];

    /**
     * Interact with the applicant status.
     */
    protected function status(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => \VettingStatus::getValue($value),
            set: fn ($value) => \VettingStatus::setValue($value),
        );
    }

    /**
     * Interact with the applicant's vettedBy.
     */
    protected function vettedBy(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => User::selectRaw(
                                    'CONCAT(first_name, " ", last_name) as vetted_by'
                                )
                                ->where('id', $value)
                                ->first()
        );
    }

    /**
     * Interact with the applicant's approvedBy.
     */
    protected function approvedBy(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => User::selectRaw(
                                    'CONCAT(first_name, " ", last_name) as approved_by'
                                )
                                ->where('id', $value)
                                ->first()
        );
    }

    /**
     * Get the user that is an applicant.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Get the employer for the applicant.
     */
    public function employer(): BelongsTo
    {
        return $this->belongsTo(Employer::class);
    }

    /**
     * Get the job for the applicant.
     */
    public function job(): BelongsTo
    {
        return $this->belongsTo(Job::class);
    }
}
