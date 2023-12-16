<?php
/**
 * Created by VS Code.
 * User: danops
 * Date: 16/12/23
 * Time: 17:52
 */

/**
 * Class UserType
 *
 * @package App\Http
 */
final class UserType
{

    const SUPER_ADMIN_ID = 1;

    const SUPER_ADMIN = '1';
    const EMPLOYER = '10';
	const APPLICANT = '20';

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
            case '10':
                $value = __('employer');
                break;
            case '20':
                $value = __('applicant');
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
            case '10':
                $value = __('Employer');
                break;
            case '20':
                $value = __('Applicant');
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

/**
 * Class VettingStatus
 */
final class VettingStatus
{
    const ACCEPTED = '10';
    const PENDING = '20';
    const REJECTED = '30';

    const SET_ACCEPTED = 'accepted';
    const SET_PENDING = 'pending';
    const SET_REJECTED = 'rejected';

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
            case '10':
                $value = __(OrderStatus::SET_ACCEPTED);
                break;
            case '20':
                $value = __(OrderStatus::SET_PENDING);
                break;
            case '30':
                $value = __(OrderStatus::SET_REJECTED);
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
            case OrderStatus::SET_ACCEPTED:
                $value = OrderStatus::ACCEPTED;
                break;
            case OrderStatus::SET_PENDING:
                $value = OrderStatus::PENDING;
                break;
            case OrderStatus::SET_REJECTED:
                $value = OrderStatus::REJECTED;
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
            self::ACCEPTED => OrderStatus::getValue(self::ACCEPTED),
            self::PENDING => OrderStatus::getValue(self::PENDING),
            self::REJECTED => OrderStatus::getValue(self::REJECTED),
        ];
    }
}