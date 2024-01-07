<?php

namespace Modules\Employer\app\Models;

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
        'user_id',
        'status'
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
     * Interact with the product's slug.
     */
    protected function slug(): Attribute
    {
        return Attribute::make(
            set: fn ($value) => $this->slugify($value),
        );
    }

    /**
     * The jobs that belong to the employer.
     */
    public function jobs(): BelongsToMany
    {
        return $this->belongsToMany(Job::class);
    }

    /**
     * Get the user that is an Employer.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Slugify employer name.
     */
    public function slugify($text)
    {
        $slug = strtolower($text);
        $slug = str_replace(array('[\', \']'), '', $slug);
        $slug = preg_replace('/\[.*\]/U', '', $slug);
        $slug = preg_replace('/&(amp;)?#?[a-z0-9]+;/i', '-', $slug);
        $slug = htmlentities($slug, ENT_COMPAT, 'utf-8');
        $slug = preg_replace('/&([a-z])(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig|quot|rsquo);/i', '\\1', $slug );
        $slug = preg_replace(array('/[^a-z0-9]/i', '/[-]+/') , '-', $slug);

        # slug repeat check
        $latest = $this->whereRaw("slug REGEXP '^{$slug}(-[0-9]+)?$'")
                        ->latest('id')
                        ->value('slug');

        if($latest){
            $pieces = explode('-', $latest);
            $number = intval(end($pieces));
            $slug .= '-' . ($number + 1);
        }       

        return $slug;
    }
}
