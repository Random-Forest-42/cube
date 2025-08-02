select
    s.person_id
    , s.best
from
    (
        select
            *
        from
            ranks_single
        where
            event_id = '333'
    ) s
    left join
    (
        select
            *
        from
            ranks_average
        where
            event_id = '333'
    ) av
    on
        s.person_id = av.person_id
where
    av.person_id is null
order by
    s.best asc