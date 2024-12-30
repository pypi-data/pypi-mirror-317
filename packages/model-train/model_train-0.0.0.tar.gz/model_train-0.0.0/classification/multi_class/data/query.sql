with comment_tab as (
    select distinct
        r.comment_id
        ,r.shop_id
        ,r.item_id
        ,i.name item_name
        ,date(r.create_datetime) create_datetime
        ,cast(
            map_from_entries(
                array[
                    ('comment_id', cast(r.comment_id as varchar))
                    ,('comment', r.comment)
                    ,('rating_star', cast(r.rating_star as varchar))
                ]
            ) as json
        ) comment_star
        ,case when CARDINALITY(split(r.comment, ' ')) between 2 and 50 then 1 else 0 end valid_comment
    from
        mp_item.dwd_item_review_df__vn_s0_live r
        left join mp_item.dim_item__vn_s0_live i on r.item_id = i.item_id
        and i.grass_date = current_date - interval '1' day
    where
        r.status in (1, 2)
        and CARDINALITY(split(r.comment, ' ')) > 1
        and r.grass_date >= date '2024-10-01'
)
,perf as (
    select
        o.item_id
        ,count(distinct o.order_id) total_orders
        ,min(date(create_datetime)) date_first_order
    from mp_order.dwd_order_item_all_ent_df__vn_s0_live o
    group by 1
)
,base as (
    select
        c.shop_id
        ,c.item_id
        ,c.item_name
        ,c.create_datetime
        ,array_agg(c.comment_star) comment_star
        ,count(distinct comment_id) total_comments
        ,count(distinct case when valid_comment = 1 then comment_id else null end) total_valid_comments
    from comment_tab c
    group by 1, 2, 3, 4
)
select
    b.*
    ,p.total_orders
    ,p.date_first_order
from
    base b
    left join perf p on p.item_id = b.item_id