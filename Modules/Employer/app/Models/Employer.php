<?php

namespace Modules\Employer\app\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

use App\Models\BaseModel;
use App\Models\User;
use Modules\Job\app\Models\Jobs;

class Employer extends BaseModel
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'employers';

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'name',
        'slug',
        'about',
        'country_id',
        'state_id',
        'address_id',
        'attachment_id',
        'status',
        'is_approved',
        'created_by',
        'approved_by',
    ];

    /**
     * Interact with the employer's status.
     */
    protected function status(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => \ActiveStatus::getValue($value),
            set: fn ($value) => \ActiveStatus::setValue($value),
        );
    }

    /**
     * Interact with the employer's slug.
     */
    protected function slug(): Attribute
    {
        return Attribute::make(
            set: fn ($value) => \slugify($this, $value),
        );
    }

    /**
     * Get the jobs for the employer.
     */
    public function jobs(): HasMany
    {
        return $this->HasMany(Job::class);
    }

    /**
     * Get the user that is an Employer.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Interact with the employercreatedBy.
     */
    protected function createdBy(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => User::selectRaw(
                                    'CONCAT(first_name, " ", last_name) as created_by'
                                )
                                ->where('id', $value)
                                ->first()
        );
    }

    /**
     * Interact with the employer's approvedBy.
     */
    protected function approvedBy(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => User::selectRaw(
                                    'CONCAT(first_name, " ", last_name) as created_by'
                                )
                                ->where('id', $value)
                                ->first()
        );
    }
}
