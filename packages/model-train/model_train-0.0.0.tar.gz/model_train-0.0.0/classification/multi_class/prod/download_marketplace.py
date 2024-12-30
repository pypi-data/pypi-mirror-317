from core_pro import DataPipeLine
from core_pro.ultilities import make_sync_folder


query = f"""
with perf as (
    select
        o.item_id
        ,count(distinct o.order_id) total_orders
    from mp_order.dwd_order_item_all_ent_df__vn_s0_live o
    where
        date(create_datetime) between date '2024-10-01' and date '2024-12-12'
        and is_bi_excluded = 0
    group by 1
    limit 1000000
)

, comment_tab as (
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
        join perf p on p.item_id = r.item_id
        left join mp_item.dim_item__vn_s0_live i on r.item_id = i.item_id
        and i.grass_date = current_date - interval '1' day
    where
        r.status in (1, 2)
        and CARDINALITY(split(r.comment, ' ')) > 1
        and date(r.create_datetime) >= date '2024-11-01'
)

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
"""

path = make_sync_folder('cx_product_review')
df = DataPipeLine(query).run_presto_to_df(save_path=path / 'raw/marketplace.parquet')
