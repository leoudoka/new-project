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