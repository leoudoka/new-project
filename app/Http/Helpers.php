<?php

use Carbon\Carbon;
use Vinkla\Hashids\Facades\Hashids;

/**
 * Get Decoded ID
 *
 * @param $encodedId
 *
 * @return int|null
 */
function getDecodedId($encodedId)
{
    $decodedArray = Hashids::decode($encodedId);
    $id = null;
    if ($decodedArray) {
        $id = $decodedArray[0];
    }

    return $id;
}


/**
 * Encode ID
 *
 * @param $id
 *
 * @return int
 */
function encodeId($id)
{
    return Hashids::encode($id);
}


/**
 * Validate date string
 *
 * @param $date
 * @param string|null $format
 *
 * @return bool
 */
function validateDate($date, $format = 'Y-m-d H:i:s')
{
    $d = DateTime::createFromFormat($format, $date);
    return $d && $d->format($format) == $date;
}


/**
 * Generate slug for string.
 *
 *
 * @return mixed|string|string[]|null
 */
function generateSlug($string)
{
    $string = strtolower(trim($string));
    $string = str_replace('-', ' ', $string);
    $string = preg_replace('/[^A-Za-z0-9-]+/', '-', $string);
    $string = str_replace(' ', '-', $string);

    return $string;
}


/**
 * Generate unique slug for entities.
 *
 *
 * @return mixed|string
 */
function slugify($entity, $text)
    {
        $slug = strtolower($text);
        $slug = str_replace(array('[\', \']'), '', $slug);
        $slug = preg_replace('/\[.*\]/U', '', $slug);
        $slug = preg_replace('/&(amp;)?#?[a-z0-9]+;/i', '-', $slug);
        $slug = htmlentities($slug, ENT_COMPAT, 'utf-8');
        $slug = preg_replace('/&([a-z])(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig|quot|rsquo);/i', '\\1', $slug );
        $slug = preg_replace(array('/[^a-z0-9]/i', '/[-]+/') , '-', $slug);

        # slug repeat check
        $latest = $entity->whereRaw("slug REGEXP '^{$slug}(-[0-9]+)?$'")
                        ->latest('id')
                        ->value('slug');

        if($latest){
            $pieces = explode('-', $latest);
            $number = intval(end($pieces));
            $slug .= '-' . ($number + 1);
        }       

        return $slug;
    }
