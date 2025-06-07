-- quiero saber como se relaciona los tiempos de 3x3 con los de 4x4
-- se me ocurren dos estadisticas, para un tiempo en especifico de 3x3, cual es la media de 4x4 de esa gente
-- para el rank de 3x3 que tiene el tiempo X, cuanto es el rank del tiempo de 4x4


-- best: el tiempo en centesimas de segundo. ej: 1800 = 18 segundos
-- ranks_average, tabla con tiempos y ranks de cada persona en cada evento, ejemplo filas:
-- #	id	person_id	event_id	best	world_rank	continent_rank	country_rank
-- 1	220413	2023EAGA01	333	1800	58971	15035	11257
-- 2	220414	2023FERI01	333	1800	58971	4728	1008
-- 3	220415	2023ORLA01	333	1800	58971	14468	746

-- select
--     *
-- from
--     ranks_average
-- where
--     event_id in ('333', '444') -- 'sq1'
--     and best >= 1800 and best < 1900
-- limit 100


select
    ranks_44.time_range
    , avg(ranks_44.world_rank_44) as avg_rank_44
    , ranks_44.world_rank_44
    , ranks_33.world_rank_33
    , (ranks_44.world_rank_44::float / ranks_33.world_rank_33) as ratio
from
(
    select
        case
            when best <= 2100 then '-21s'
            when best >= 2100 and best < 2300 then '21s-23s'
            when best >= 2300 and best < 2500 then '23s-25s'
            when best >= 2500 and best < 2700 then '25s-27s'
            when best >= 2700 and best < 2900 then '27s-29s'
            when best >= 2900 and best < 3100 then '29s-31s'
            when best >= 3100 and best < 3300 then '31s-33s'
            when best >= 3300 and best < 3500 then '33s-35s'
            when best >= 3500 and best < 3700 then '35s-37s'
            when best >= 3700 and best < 3900 then '37s-39s'
            when best >= 3900 and best < 4100 then '39s-41s'
            when best >= 4100 and best < 4300 then '41s-43s'
            when best >= 4300 and best < 4500 then '43s-45s'
            when best >= 4500 and best < 4700 then '45s-47s'
            when best >= 4700 and best < 4900 then '47s-49s'
            when best >= 4900 and best < 5100 then '49s-51s'
            when best >= 5100 and best < 5300 then '51s-53s'
            when best >= 5300 and best < 5500 then '53s-55s'
            when best >= 5500 and best < 5700 then '55s-57s'
            when best >= 5700 and best < 5900 then '57s-59s'
            when best >= 5900 and best < 6100 then '59s-61s'
            when best >= 6100 and best < 6300 then '61s-63s'
            when best >= 6300 and best < 6500 then '63s-65s'
            when best >= 6500 and best < 6700 then '65s-67s'
            when best >= 6700 and best < 6900 then '67s-69s'
            when best >= 6900 and best < 7100 then '69s-71s'
            when best >= 7100 and best < 7300 then '71s-73s'
            when best >= 7300 and best < 7500 then '73s-75s'
            when best >= 7500 and best < 7700 then '75s-77s'
            when best >= 7700 and best < 7900 then '77s-79s'
            when best >= 7900 and best < 8100 then '79s-81s'
            when best >= 8100 and best < 8300 then '81s-83s'
            when best >= 8300 and best < 8500 then '83s-85s'
            when best >= 8500 and best < 8700 then '85s-87s'
            when best >= 8700 and best < 8900 then '87s-89s'
            when best >= 8900 and best < 9100 then '89s-91s'
            when best >= 9100 and best < 9300 then '91s-93s'
            when best >= 9300 and best < 9500 then '93s-95s'
            when best >= 9500 and best < 9700 then '95s-97s'
            when best >= 9700 and best < 9900 then '97s-99s'
            when best >= 9900 and best < 10100 then '99s-101s'
            when best >= 10100 and best < 10300 then '101s-103s'
            when best >= 10300 and best < 10500 then '103s-105s'
            when best >= 10500 and best < 10700 then '105s-107s'
            when best >= 10700 and best < 10900 then '107s-109s'
            when best >= 10900 and best < 11100 then '109s-111s'
            when best >= 11100 and best < 11300 then '111s-113s'
            when best >= 11300 and best < 11500 then '113s-115s'
            when best >= 11500 and best < 11700 then '115s-117s'
            when best >= 11700 and best < 11900 then '117s-119s'
            else '119+'


        end as time_range
        , min(world_rank) as world_rank_44
    from
        ranks_average
    where
        event_id = '444'
        and best >= 2100 and best < 20000
    group by
        time_range
) ranks_44
inner join
(
    select
        case
            when best >= 900 and best < 1000 then '9s-10s'
            when best >= 1000 and best < 1100 then '10s-11s'
            when best >= 1100 and best < 1200 then '11s-12s'
            when best >= 1200 and best < 1300 then '12s-13s'
            when best >= 1300 and best < 1400 then '13s-14s'
            when best >= 1400 and best < 1500 then '14s-15s'
            when best >= 1500 and best < 1600 then '15s-16s'
            when best >= 1600 and best < 1700 then '16s-17s'
            when best >= 1700 and best < 1800 then '17s-18s'
            when best >= 1800 and best < 1900 then '18s-19s'
            when best >= 1900 and best < 2000 then '19s-20s'
            when best >= 2000 and best < 2100 then '20s-21s'
            when best >= 2100 and best < 2200 then '21s-22s'
            else '2200+'
        end as time_range
        , min(world_rank) as world_rank_33
    from
        ranks_average
    where
        event_id = '333'
        and best >= 900 and best < 2200
    group by
        time_range
) as ranks_33
on
    ranks_33.time_range = ranks_44.time_range



-- idea 2: de los que hacen 3x3 entre x, x+1 segundos, cuanto hacen en 4x4

select
    ranks_33.time_range as time_33
    , avg(ranks_44.world_rank) as avg_rank_44
    -- , median(ranks_44.world_rank) as median_rank_44
    , round(avg(ranks_44.best) / 100, 2) as avg_best_44
    , count(1) as personas
from
(
    select
        case
            when best >= 900 and best < 1000 then '00:9s-10s'
            when best >= 1000 and best < 1100 then '01:10s-11s'
            when best >= 1100 and best < 1200 then '02:11s-12s'
            when best >= 1200 and best < 1300 then '03:12s-13s'
            when best >= 1300 and best < 1400 then '04:13s-14s'
            when best >= 1400 and best < 1500 then '05:14s-15s'
            when best >= 1500 and best < 1600 then '06:15s-16s'
            when best >= 1600 and best < 1700 then '07:16s-17s'
            when best >= 1700 and best < 1800 then '08:17s-18s'
            when best >= 1800 and best < 1900 then '09:18s-19s'
            when best >= 1900 and best < 2000 then '10:19s-20s'
            when best >= 2000 and best < 2100 then '11:20s-21s'
            when best >= 2100 and best < 2200 then '12:21s-22s'
            else '2200+'
        end as time_range
        , world_rank
        , person_id as wca_id
        , best
    from
        ranks_average
    where
        event_id = '333'
        and best >= 900 and best < 2200
) as ranks_33
inner join
(
    select
        case
            when best <= 2100 then '-21s'
            when best >= 2100 and best < 2300 then '21s-23s'
            when best >= 2300 and best < 2500 then '23s-25s'
            when best >= 2500 and best < 2700 then '25s-27s'
            when best >= 2700 and best < 2900 then '27s-29s'
            when best >= 2900 and best < 3100 then '29s-31s'
            when best >= 3100 and best < 3300 then '31s-33s'
            when best >= 3300 and best < 3500 then '33s-35s'
            when best >= 3500 and best < 3700 then '35s-37s'
            when best >= 3700 and best < 3900 then '37s-39s'
            when best >= 3900 and best < 4100 then '39s-41s'
            when best >= 4100 and best < 4300 then '41s-43s'
            when best >= 4300 and best < 4500 then '43s-45s'
            when best >= 4500 and best < 4700 then '45s-47s'
            when best >= 4700 and best < 4900 then '47s-49s'
            when best >= 4900 and best < 5100 then '49s-51s'
            when best >= 5100 and best < 5300 then '51s-53s'
            when best >= 5300 and best < 5500 then '53s-55s'
            when best >= 5500 and best < 5700 then '55s-57s'
            when best >= 5700 and best < 5900 then '57s-59s'
            when best >= 5900 and best < 6100 then '59s-61s'
            when best >= 6100 and best < 6300 then '61s-63s'
            when best >= 6300 and best < 6500 then '63s-65s'
            when best >= 6500 and best < 6700 then '65s-67s'
            when best >= 6700 and best < 6900 then '67s-69s'
            when best >= 6900 and best < 7100 then '69s-71s'
            when best >= 7100 and best < 7300 then '71s-73s'
            when best >= 7300 and best < 7500 then '73s-75s'
            when best >= 7500 and best < 7700 then '75s-77s'
            when best >= 7700 and best < 7900 then '77s-79s'
            when best >= 7900 and best < 8100 then '79s-81s'
            when best >= 8100 and best < 8300 then '81s-83s'
            when best >= 8300 and best < 8500 then '83s-85s'
            when best >= 8500 and best < 8700 then '85s-87s'
            when best >= 8700 and best < 8900 then '87s-89s'
            when best >= 8900 and best < 9100 then '89s-91s'
            when best >= 9100 and best < 9300 then '91s-93s'
            when best >= 9300 and best < 9500 then '93s-95s'
            when best >= 9500 and best < 9700 then '95s-97s'
            when best >= 9700 and best < 9900 then '97s-99s'
            when best >= 9900 and best < 10100 then '99s-101s'
            when best >= 10100 and best < 10300 then '101s-103s'
            when best >= 10300 and best < 10500 then '103s-105s'
            when best >= 10500 and best < 10700 then '105s-107s'
            when best >= 10700 and best < 10900 then '107s-109s'
            when best >= 10900 and best < 11100 then '109s-111s'
            when best >= 11100 and best < 11300 then '111s-113s'
            when best >= 11300 and best < 11500 then '113s-115s'
            when best >= 11500 and best < 11700 then '115s-117s'
            when best >= 11700 and best < 11900 then '117s-119s'
            else '119+'
        end as time_range
        , world_rank
        , best
        , person_id as wca_id
    from
        ranks_average
    where
        event_id = '444'
) ranks_44
on
    ranks_33.wca_id = ranks_44.wca_id
-- where
--     ranks_33.time_range >= 1500 and ranks_33.best < 2200
--     and ranks_44.best >= 2100 and ranks_44.best < 20000
group by 1



select
    ranks_other_event.event_id
    , ranks_33.time_range as time_33
    , avg(ranks_other_event.world_rank) as avg_rank_other_event
    , round(avg(ranks_other_event.best) / 100, 2) as avg_best_other_event
    , count(1) as personas
from
    (
        select
            case
                when best >= 900 and best < 1000 then '00:9s-10s'
                when best >= 1000 and best < 1100 then '01:10s-11s'
                when best >= 1100 and best < 1200 then '02:11s-12s'
                when best >= 1200 and best < 1300 then '03:12s-13s'
                when best >= 1300 and best < 1400 then '04:13s-14s'
                when best >= 1400 and best < 1500 then '05:14s-15s'
                when best >= 1500 and best < 1600 then '06:15s-16s'
                when best >= 1600 and best < 1700 then '07:16s-17s'
                when best >= 1700 and best < 1800 then '08:17s-18s'
                when best >= 1800 and best < 1900 then '09:18s-19s'
                when best >= 1900 and best < 2000 then '10:19s-20s'
                when best >= 2000 and best < 2100 then '11:20s-21s'
                when best >= 2100 and best < 2200 then '12:21s-22s'
                else '2200+'
            end as time_range
            , world_rank
            , person_id as wca_id
            , best
        from
            ranks_average
        where
            event_id = '333'
            and best >= 900 and best < 2200
    ) as ranks_33
    inner join
    (
        select
            world_rank
            , best
            , person_id as wca_id
            , event_id
        from
            ranks_average
        where
            event_id in ('clock', '444', 'sq1', '222')
    ) ranks_other_event
    on
        ranks_33.wca_id = ranks_other_event.wca_id
group by 1, 2
order by 1, 2 asc
