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

    const SUPER_ADMIN = 1;
    const EMPLOYER = 10;
	const APPLICANT = 20;

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
            case 1:
                $value = __('super-admin');
                break;
            case 10:
                $value = __('employer');
                break;
            case 20:
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
            case 1:
                $value = __('Super Admin');
                break;
            case 10:
                $value = __('Employer');
                break;
            case 20:
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
    CONST MALE = 10;
    CONST FEMALE = 20;
    CONST NOT_SPECIFIED = 30;

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
            case 10:
                $value = 'male';
                break;
            case 20:
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
    const INACTIVE = 0;
    const ACTIVE = 1;

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
            case 0:
                $value = __(ActiveStatus::SET_INACTIVE);
                break;
            case 1:
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
 * Class JobStatus
 */
final class JobStatus
{
    const NEW = 10;
    const OPEN = 20;
    const CLOSED = 30;

    const SET_NEW = 'new';
    const SET_OPEN = 'open';
    const SET_CLOSED = 'closed';

    /**
     * Returns respective value.
     *
     * @param $x
     *
     * @return null
     */
    public static function getValue($jobCode)
    {
        $value = null;
        switch ($jobCode) {
            case 10:
                $value = __(JobStatus::SET_NEW);
                break;
            case 20:
                $value = __(JobStatus::SET_OPEN);
                break;
            case 30:
                $value = __(JobStatus::SET_CLOSED);
                break;
        }

        return $value;
    }

    /**
     * Returns respective value.
     * 
     * @return array|null
     */
    public static function setValue($jobCode)
    {
        $value = null;
        switch ($jobCode) {
            case JobStatus::SET_NEW:
                $value = JobStatus::NEW;
                break;
            case JobStatus::SET_OPEN:
                $value = JobStatus::OPEN;
                break;
            case JobStatus::SET_CLOSED:
                $value = JobStatus::CLOSED;
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
    const ACCEPTED = 10;
    const PENDING = 20;
    const REJECTED = 30;

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
            case 10:
                $value = __(OrderStatus::SET_ACCEPTED);
                break;
            case 20:
                $value = __(OrderStatus::SET_PENDING);
                break;
            case 30:
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


/**
 * Class JobExperienceLevelType
 */
final class JobExperienceLevelType
{
    const ANY_YEARS_OF_EXPERIENCE = 'any-years-of-experience';
    const NO_EXPERIENCE = 'no-experience';
    const INTERNSHIP_GRADUATE = 'internship-graduate';
    const ENTRY_LEVEL = 'entry-level';
    const MID_LEVEL = 'mid-level';
    const SENIOR_LEVEL = 'senior-level';

    const SET_ANY_YEARS_OF_EXPERIENCE = 'Any Years of Experience';
    const SET_NO_EXPERIENCE = 'No Experience';
    const SET_INTERNSHIP_GRADUATE = 'Internship Graduate';
    const SET_ENTRY_LEVEL = 'Entry Level';
    const SET_MID_LEVEL = 'Mid Level';
    const SET_SENIOR_LEVEL = 'Senior Level';

    /**
     * Returns respective value.
     *
     * @param $x
     *
     * @return null
     */
    public static function getValue($experienceLevel)
    {
        $value = null;
        switch ($experienceLevel) {
            case JobExperienceLevelType::ANY_YEARS_OF_EXPERIENCE:
                $value = __(JobExperienceLevelType::SET_ANY_YEARS_OF_EXPERIENCE);
                break;
            case JobExperienceLevelType::NO_EXPERIENCE:
                $value = __(JobExperienceLevelType::SET_NO_EXPERIENCE);
                break;
            case JobExperienceLevelType::INTERNSHIP_GRADUATE:
                $value = __(JobExperienceLevelType::SET_INTERNSHIP_GRADUATE);
                break;
            case JobExperienceLevelType::ENTRY_LEVEL:
                $value = __(JobExperienceLevelType::SET_ENTRY_LEVEL);
                break;
            case JobExperienceLevelType::MID_LEVEL:
                $value = __(JobExperienceLevelType::SET_MID_LEVEL);
                break;
            case JobExperienceLevelType::SENIOR_LEVEL_LEVEL:
                $value = __(JobExperienceLevelType::SET_SENIOR_LEVEL_LEVEL);
                break;
        }

        return $value;
    }

    /**
     * Returns respective value.
     * 
     * @return array|null
     */
    public static function setValue($experienceLevel)
    {
        $value = null;
        switch ($experienceLevel) {
            case JobExperienceLevelType::SET_ANY_YEARS_OF_EXPERIENCE:
                $value = JobExperienceLevelType::ANY_YEARS_OF_EXPERIENCE;
                break;
            case JobExperienceLevelType::SET_NO_EXPERIENCE:
                $value = JobExperienceLevelType::NO_EXPERIENCE;
                break;
            case JobExperienceLevelType::SET_INTERNSHIP_GRADUATE:
                $value = JobExperienceLevelType::INTERNSHIP_GRADUATE;
                break;
            case JobExperienceLevelType::SET_ENTRY_LEVEL:
                $value = JobExperienceLevelType::ENTRY_LEVEL;
                break;
            case JobExperienceLevelType::SET_MID_LEVEL:
                $value = JobExperienceLevelType::MID_LEVEL;
                break;
            case JobExperienceLevelType::SET_SENIOR_LEVEL:
                $value = JobExperienceLevelType::SENIOR_LEVEL;
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
            self::ANY_YEARS_OF_EXPERIENCE => JobExperienceLevelType::getValue(self::ANY_YEARS_OF_EXPERIENCE),
            self::NO_EXPERIENCE => JobExperienceLevelType::getValue(self::NO_EXPERIENCE),
            self::INTERNSHIP_GRADUATE => JobExperienceLevelType::getValue(self::INTERNSHIP_GRADUATE),
            self::ENTRY_LEVEL => JobExperienceLevelType::getValue(self::ENTRY_LEVEL),
            self::MID_LEVEL => JobExperienceLevelType::getValue(self::MID_LEVEL),
            self::SENIOR_LEVEL => JobExperienceLevelType::getValue(self::SENIOR_LEVEL),
        ];
    }

    /**
     * @return array
     */
    public static function setAll()
    {
        return [
            self::SET_ANY_YEARS_OF_EXPERIENCE => JobExperienceLevelType::getValue(self::SET_ANY_YEARS_OF_EXPERIENCE),
            self::SET_NO_EXPERIENCE => JobExperienceLevelType::getValue(self::SET_NO_EXPERIENCE),
            self::SET_INTERNSHIP_GRADUATE => JobExperienceLevelType::getValue(self::SET_INTERNSHIP_GRADUATE),
            self::SET_ENTRY_LEVEL => JobExperienceLevelType::getValue(self::SET_ENTRY_LEVEL),
            self::SET_MID_LEVEL => JobExperienceLevelType::getValue(self::SET_MID_LEVEL),
            self::SET_SENIOR_LEVEL => JobExperienceLevelType::getValue(self::SET_SENIOR_LEVEL),
        ];
    }
}


/**
 * Class JobTypeK
 */
final class JobTypeK
{
    const CONTRACT = 'contract';
    const FULL_GRADUATE = 'full-graduate';
    const INTERNSHIP_GRADUATE = 'internship-graduate';
    const PART_TIME = 'part-time';

    const SET_CONTRACT = 'Contract';
    const SET_FULL_GRADUATE = 'Full Graduate';
    const SET_INTERNSHIP_GRADUATE = 'Internship Graduate';
    const SET_PART_TIME = 'Part Time';

    /**
     * Returns respective value.
     *
     * @param $x
     *
     * @return null
     */
    public static function getValue($experienceLevel)
    {
        $value = null;
        switch ($experienceLevel) {
            case JobTypeK::CONTRACT:
                $value = __(JobTypeK::SET_CONTRACT);
                break;
            case JobTypeK::FULL_GRADUATE:
                $value = __(JobTypeK::SET_FULL_GRADUATE);
                break;
            case JobTypeK::INTERNSHIP_GRADUATE:
                $value = __(JobTypeK::SET_INTERNSHIP_GRADUATE);
                break;
            case JobTypeK::PART_TIME:
                $value = __(JobTypeK::SET_PART_TIME);
                break;
        }

        return $value;
    }

    /**
     * Returns respective value.
     * 
     * @return array|null
     */
    public static function setValue($experienceLevel)
    {
        $value = null;
        switch ($experienceLevel) {
            case JobTypeK::SET_CONTRACT:
                $value = JobTypeK::NO_CONTRACT;
                break;
            case JobTypeK::SET_FULL_GRADUATE:
                $value = JobTypeK::FULL_GRADUATE;
                break;
            case JobTypeK::SET_INTERNSHIP_GRADUATE:
                $value = JobTypeK::INTERNSHIP_GRADUATE;
                break;
            case JobTypeK::SET_PART_TIME:
                $value = JobTypeK::PART_TIME;
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
            self::NO_EXPERIENCE => JobTypeK::getValue(self::NO_EXPERIENCE),
            self::FULL_GRADUATE => JobTypeK::getValue(self::FULL_GRADUATE),
            self::INTERNSHIP_GRADUATE => JobTypeK::getValue(self::INTERNSHIP_GRADUATE),
            self::PART_TIME => JobTypeK::getValue(self::PART_TIME)
        ];
    }

    /**
     * @return array
     */
    public static function setAll()
    {
        return [
            self::SET_NO_EXPERIENCE => JobTypeK::getValue(self::SET_NO_EXPERIENCE),
            self::SET_FULL_GRADUATE => JobTypeK::getValue(self::SET_FULL_GRADUATE),
            self::SET_INTERNSHIP_GRADUATE => JobTypeK::getValue(self::SET_INTERNSHIP_GRADUATE),
            self::SET_PART_TIME => JobTypeK::getValue(self::SET_PART_TIME),
            self::SET_SENIOR_LEVEL => JobTypeK::getValue(self::SET_SENIOR_LEVEL),
        ];
    }
}