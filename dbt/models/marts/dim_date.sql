with date_spine as (

    select
        dateadd(
            day,
            seq4(),
            '2020-01-01'::date
        ) as full_date

    from table(generator(rowcount => 5000))

),

final as (

    select
        to_number(to_char(full_date, 'YYYYMMDD')) as date_key,
        full_date,

        year(full_date) as year,
        quarter(full_date) as quarter,

        month(full_date) as month_number,
        monthname(full_date) as month_name,

        day(full_date) as day_of_month,
        dayofweekiso(full_date) as day_of_week,
        dayname(full_date) as day_name,

        weekiso(full_date) as week_of_year,

        case
            when dayofweekiso(full_date) in (6, 7) then true
            else false
        end as is_weekend,

        date_trunc('week', full_date) as week_start_date,
        last_day(full_date, 'month') as month_end_date,

        case
            when full_date = last_day(full_date, 'month') then true
            else false
        end as is_last_day_of_month

    from date_spine

)

select *
from final