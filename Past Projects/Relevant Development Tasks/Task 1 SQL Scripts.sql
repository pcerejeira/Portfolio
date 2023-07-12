-- To check the SQL expression I created this script:

WITH temp AS (
    SELECT
        commercial_designation,
        regexp_matches(commercial_designation, '(\d{2})') as power,
        reverse(commercial_designation) as reversed_commercial_designation,
        regexp_matches(reverse(commercial_designation), '(\d{2})') as capacity,
        array_length(regexp_matches(commercial_designation, '\d{4}'), 1) as count_numbers
    FROM
        product p
)
SELECT
	distinct
    commercial_designation,
    power[1] as power,
    reverse(capacity[1]) as capacity
FROM
    temp
where
	count_numbers = 1

-- To populate the product table, the following script can be used:

WITH temp AS (
    SELECT
        commercial_designation,
        regexp_matches(commercial_designation, '(\d{2})') as power,
        reverse(commercial_designation) as reversed_commercial_designation,
        regexp_matches(reverse(commercial_designation), '(\d{2})') as capacity,
        array_length(regexp_matches(commercial_designation, '\d{4}'), 1) as count_numbers
    FROM
        product p
)
UPDATE
    product
SET
    power = cast(temp.power[1] as real),
    capacity = cast(reverse(temp.capacity[1]) as real)
FROM
    temp
WHERE
    product.commercial_designation = temp.commercial_designation and count_numbers = 1

-- To populate the production_project table:

WITH temp AS (
    SELECT
        commercial_designation,
        regexp_matches(commercial_designation, '(\d{2})') as power,
        reverse(commercial_designation) as reversed_commercial_designation,
        regexp_matches(reverse(commercial_designation), '(\d{2})') as capacity,
        array_length(regexp_matches(commercial_designation, '\d{4}'), 1) as count_numbers
    FROM
        production_project p
)
UPDATE
    production_project
SET
    power = cast(temp.power[1] as real),
    capacity = cast(reverse(temp.capacity[1]) as real)
FROM
    temp
WHERE
    production_project.commercial_designation = temp.commercial_designation and count_numbers = 1