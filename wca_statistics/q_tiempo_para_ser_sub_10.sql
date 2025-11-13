/* ahora nos fijamos en los que son sub 10 en especifico, y los tramificamos en cuanto han tardado en ser sub X */


select
    time_range_prev
    , avg(total_competiciones) as avg_total_competiciones
    , avg(competiciones_hasta_record) as avg_competiciones_hasta_record
    , avg(avg_hasta_record) as avg_avg_hasta_record
    , avg(competiciones_despues_record) as avg_competiciones_despues_record
    , avg(avg_despues_record) as avg_avg_despues_record
from
(
    select
        wca_id
        , case
            when average >= 500 and average < 600 then '01:5s-6s'
            when average >= 600 and average < 700 then '02:6s-7s'
            when average >= 700 and average < 800 then '03:7s-8s'
            when average >= 800 and average < 900 then '04:8s-9s'
            when average >= 900 and average < 1000 then '05:9s-10s'
            when average >= 1000 and average < 1100 then '06:10s-11s'
            when average >= 1100 and average < 1200 then '07:11s-12s'
            when average >= 1200 and average < 1300 then '08:12s-13s'
            when average >= 1300 and average < 1400 then '09:13s-14s'
            when average >= 1400 and average < 1500 then '10:14s-15s'
            when average >= 1500 and average < 1600 then '11:15s-16s'
            when average >= 1600 and average < 1700 then '12:16s-17s'
            when average >= 1700 and average < 1800 then '13:17s-18s'
            when average >= 1800 and average < 1900 then '14:18s-19s'
            when average >= 1900 and average < 2000 then '15:19s-20s'
            when average >= 2000 and average < 2100 then '16:20s-21s'
            when average >= 2100 and average < 2200 then '17:21s-22s'
            when average >= 2200 and average < 2300 then '18:22s-23s'
            when average >= 2300 and average < 2400 then '19:23s-24s'
            else '2400+'
        end as time_range_prev
        , count(1) as total_competiciones
        , sum(case when result_id < record_result_id then 1 else 0 end) as competiciones_hasta_record
        , avg(case when result_id < record_result_id then average else null end) as avg_hasta_record
        , sum(case when result_id > record_result_id then 1 else 0 end) as competiciones_despues_record
        , avg(case when result_id > record_result_id then average else null end) as avg_despues_record
    from
    (
        select
            ranks_33.wca_id
            , ranks_33.best
            , ranks_33.time_range
            , events_33.average
            , events_33.id as result_id
            , record_result_id
        from
        (
            select
                best
                , world_rank
                , person_id as wca_id
                , case
                    when best >= 500 and best < 600 then '01:5s-6s'
                    when best >= 600 and best < 700 then '02:6s-7s'
                    when best >= 700 and best < 800 then '03:7s-8s'
                    when best >= 800 and best < 900 then '04:8s-9s'
                    when best >= 900 and best < 1000 then '05:9s-10s'
                    when best >= 1000 and best < 1100 then '06:10s-11s'
                    when best >= 1100 and best < 1200 then '07:11s-12s'
                    when best >= 1200 and best < 1300 then '08:12s-13s'
                    when best >= 1300 and best < 1400 then '09:13s-14s'
                    when best >= 1400 and best < 1500 then '10:14s-15s'
                    when best >= 1500 and best < 1600 then '11:15s-16s'
                    when best >= 1600 and best < 1700 then '12:16s-17s'
                    when best >= 1700 and best < 1800 then '13:17s-18s'
                    when best >= 1800 and best < 1900 then '14:18s-19s'
                    when best >= 1900 and best < 2000 then '15:19s-20s'
                    when best >= 2000 and best < 2100 then '16:20s-21s'
                    when best >= 2100 and best < 2200 then '17:21s-22s'
                    when best >= 2200 and best < 2300 then '18:22s-23s'
                    when best >= 2300 and best < 2400 then '19:23s-24s'
                    else '2400+'
                end as time_range
            from
                ranks_average
            where
                event_id = '333'
                and best >= 900 and best < 1000
        ) as ranks_33
        inner join
        (
            select
                person_id as wca_id
                , average
                , id
            from
                results
            where
                event_id = '333'
                and average < 4000
        ) as events_33
        on
            ranks_33.wca_id = events_33.wca_id
        inner join
        (
            select
                ranks_33.wca_id
                , min(ranks_33.best) as best
                , min(events_33.id) as record_result_id
            from
            (
                select
                    best
                    , world_rank
                    , person_id as wca_id
                from
                    ranks_average
                where
                    event_id = '333'
                    and best >= 800 and best < 2000
            ) as ranks_33
            inner join
            (
                select
                    person_id as wca_id
                    , average
                    , id
                from
                    results
                where
                    event_id = '333'
                    and average < 4000
            ) as events_33
            on
                ranks_33.wca_id = events_33.wca_id
            where
                events_33.average = ranks_33.best
            group by
                ranks_33.wca_id
        ) rec_33
        on
            ranks_33.wca_id = rec_33.wca_id
        where
            id < record_result_id /* nos quedamos con competiciones anteriores */
    ) a
    group by
        wca_id
        , time_range_prev
) b
where
    total_competiciones > 10
group by
    time_range_prev
order by
    time_range_prev asc


#	time_range_prev	avg_total_competiciones	avg_competiciones_hasta_record	avg_avg_hasta_record	avg_competiciones_despues_record	avg_avg_despues_record
1	05:9s-10s	16.5857	16.5857	967.90190857	0.0000
2	06:10s-11s	21.3921	21.3921	1055.80727093	0.0000
3	07:11s-12s	23.7697	23.7697	1148.29743135	0.0000
4	08:12s-13s	22.9695	22.9695	1245.59965986	0.0000
5	09:13s-14s	18.7709	18.7709	1344.19204473	0.0000
6	10:14s-15s	16.0211	16.0211	1443.56205789	0.0000
7	11:15s-16s	15.5000	15.5000	1547.32130000	0.0000
8	12:16s-17s	12.9091	12.9091	1648.86400909	0.0000
9	13:17s-18s	16.0000	16.0000	1729.68750000	0.0000
10	2400+	13.6667	13.6667	2332.24880000	0.0000
