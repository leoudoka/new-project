<?php
/**
 * Created by VS Code.
 * User: danops
 * Date: 16/12/23
 * Time: 17:52
 */

/**
 * Class EntityType
 *
 * @package App\Http
 */
final class UserType
{

    const SUPER_ADMIN_ID = 1;

    const SUPER_ADMIN = '1';

    /**
     * Returns respective value.
     *
     * @param $x
     *
     * @return null
     */
    public static function getValue($x)
    {
        $value = null;
        switch ($x) {
            case '1':
                $value = __('super-admin');
                break;
        }

        return $value;
    }

    /**
     * Returns respective value.
     *
     * @param $x
     *
     * @return null
     */
    public static function getValueBladeTemplate($x)
    {
        $value = null;
        switch ($x) {
            case '1':
                $value = __('Super Admin');
                break;
        }

        return $value;
    }
}

/**
 * Class Gender
 */
final class Gender
{
    CONST MALE = '10';
    CONST FEMALE = '20';
    CONST NOT_SPECIFIED = '30';

    /**
     * Returns respective value.
     *
     * @param $x
     *
     * @return null
     */
    public static function getValue($x)
    {
        $value = null;
        switch ($x) {
            case '10':
                $value = 'male';
                break;
            case '20':
                $value = 'female';
                break;
        }

        return $value;
    }

    /**
     * @return array
     */
    public static function getAll()
    {
        return [
            self::MALE => Gender::getValue(self::MALE),
            self::FEMALE => Gender::getValue(self::FEMALE),
        ];
    }
}

/**
 * Class ActiveStatus
 */
final class ActiveStatus
{
    const INACTIVE = '0';
    const ACTIVE = '1';

    const SET_INACTIVE = 'inactive';
    const SET_ACTIVE = 'active';

    /**
     * Returns respective value.
     *
     * @param $x
     *
     * @return null
     */
    public static function getValue($statusCode)
    {
        $value = null;
        switch ($statusCode) {
            case '0':
                $value = __(ActiveStatus::SET_INACTIVE);
                break;
            case '1':
                $value = __(ActiveStatus::SET_ACTIVE);
                break;
        }

        return $value;
    }

    /**
     * Returns respective value.
     * 
     * @return array|null
     */
    public static function setValue($statusCode)
    {
        $value = null;
        switch ($statusCode) {
            case ActiveStatus::SET_INACTIVE:
                $value = ActiveStatus::INACTIVE;
                break;
            case ActiveStatus::SET_ACTIVE:
                $value = ActiveStatus::ACTIVE;
                break;
        }

        return $value;
    }
}