select
    a.event_id
    , count(1) as total_spain
    , max(case when best < 500 then country_rank else 0 end) as sub_5
from
    (
        select
            *
        from
            ranks_average
        where
            event_id = 333
    ) a
    inner join
    (
        select
            id
        from
            persons
        where
            country_id = 'Spain'
            and sub_id = 1
    ) c
    on
    a.id = c.id
