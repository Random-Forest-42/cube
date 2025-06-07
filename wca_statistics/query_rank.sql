select
    a.event_id
    , count(1) as total_spain
    , max(case when best < 500 then country_rank else 0 end) as sub_5
    , max(case when best < 600 then country_rank else 0 end) as sub_6
    , max(case when best < 700 then country_rank else 0 end) as sub_7
    , max(case when best < 800 then country_rank else 0 end) as sub_8
    , max(case when best < 900 then country_rank else 0 end) as sub_9
    , max(case when best < 1000 then country_rank else 0 end) as sub_10
    , max(case when best < 1100 then country_rank else 0 end) as sub_11
    , max(case when best < 1200 then country_rank else 0 end) as sub_12
    , max(case when best < 1300 then country_rank else 0 end) as sub_13
    , max(case when best < 1400 then country_rank else 0 end) as sub_14
    , max(case when best < 1500 then country_rank else 0 end) as sub_15
    , max(case when best < 1600 then country_rank else 0 end) as sub_16
    , max(case when best < 1700 then country_rank else 0 end) as sub_17
    , max(case when best < 1800 then country_rank else 0 end) as sub_18
    , max(case when best < 1900 then country_rank else 0 end) as sub_19
    , max(case when best < 2000 then country_rank else 0 end) as sub_20
    , max(case when best < 2100 then country_rank else 0 end) as sub_21
    , max(case when best < 2200 then country_rank else 0 end) as sub_22
    , max(case when country_rank = 1 then best else 0 end) as top_1
    , max(case when country_rank <= 10 then best else 0 end) as top_10
    , max(case when country_rank <= 100 then best else 0 end) as top_100
    , max(case when country_rank <= 200 then best else 0 end) as top_200
    , max(case when country_rank <= 300 then best else 0 end) as top_300
    , max(case when country_rank <= 400 then best else 0 end) as top_400
    , max(case when country_rank <= 500 then best else 0 end) as top_500
    , max(case when country_rank <= 600 then best else 0 end) as top_600
    , max(case when country_rank <= 700 then best else 0 end) as top_700
    , max(case when country_rank <= 800 then best else 0 end) as top_800
    , max(case when country_rank <= 900 then best else 0 end) as top_900
    , max(case when country_rank <= 1000 then best else 0 end) as top_1000
    , max(case when country_rank <= 1100 then best else 0 end) as top_1100
    , max(case when country_rank <= 1200 then best else 0 end) as top_1200
    , max(case when country_rank <= 1300 then best else 0 end) as top_1300
    , max(case when country_rank <= 1400 then best else 0 end) as top_1400
    , max(case when country_rank <= 1500 then best else 0 end) as top_1500
    , max(case when country_rank <= 1600 then best else 0 end) as top_1600
    , max(case when country_rank <= 1700 then best else 0 end) as top_1700
    , max(case when country_rank <= 1800 then best else 0 end) as top_1800
    , max(case when country_rank <= 1900 then best else 0 end) as top_1900
    , max(case when country_rank <= 2000 then best else 0 end) as top_2000
from
    (
        select
            *
        from
            ranks_average
        where
            -- event_id = '333'
            event_id = 'sq1'
    ) a
    inner join
    (
        select
            wca_id
        from
            persons
        where
            country_id = 'Spain'
            and sub_id = 1
and sub_id = 1
    ) c
    on
    a.person_id = c.wca_id
