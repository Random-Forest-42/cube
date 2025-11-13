select
    wcas.*
    , average_33.best as best_average_33
    , single_33.best as best_single_33
from
    (
        select
            u.wca_id
            , u.name
        from
            (
                select
                    user_id
                from
                    registrations
                where
                    competition_id = 'wc2025'
                    and id in
                    (
                        select
                            registration_id
                        from
                            registration_competition_events
                        where
                            competition_event_id in
                            (
                                select
                                    id
                                from
                                    competition_events
                                where
                                    competition_id = 'wc2025'
                                    and event_id = '333'
                        )
                    )
            ) comp_33
            inner join users u
            on
                comp_33.user_id = u.id
    ) wcas
    left join
    (
        select
            best
            , person_id as wca_id
        from
            ranks_average
        where
            event_id = '333'
    ) average_33
    on
        wcas.wca_id = average_33.wca_id
    left join
    (
        select
            best
            , person_id as wca_id
        from
            ranks_single
        where
            event_id = '333'
    ) single_33
    on
        wcas.wca_id = single_33.wca_id

order by
    best_average_33 asc




select
    wcas.*
    , average_33.best as best_average_33
from
    (
        select
            u.wca_id
            , u.name
        from
            (
                select
                    user_id
                from
                    registrations
                where
                    competition_id = 'wc2025'
                    and id in
                    (
                        select
                            registration_id
                        from
                            registration_competition_events
                        where
                            competition_event_id in
                            (
                                select
                                    id
                                from
                                    competition_events
                                where
                                    competition_id = 'wc2025'
                                    and event_id = '333'
                        )
                    )
            ) comp_33
            inner join users u
            on
                comp_33.user_id = u.id
    ) wcas
    left join
    (
        select
            best
            , person_id as wca_id
        from
            ranks_average
        where
            event_id = '333'
    ) average_33
    on
        wcas.wca_id = average_33.wca_id

order by
    best_average_33 asc
