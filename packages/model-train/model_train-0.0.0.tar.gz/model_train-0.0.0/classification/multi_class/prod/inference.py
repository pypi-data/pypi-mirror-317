from pathlib import Path
import duckdb
import polars as pl
from rich import print
from core_pro.ultilities import make_dir, make_sync_folder, upload_to_datahub

import sys
sys.path.extend([str(Path.home() / 'PycharmProjects/model_train')])
from src.model_train.pipeline_infer import InferenceTextClassification, data_batching


# init
path = make_sync_folder('cx_product_review')
file_raw = path / 'raw/choice_sbs.parquet'

path_export_inference = path / f'inference/{file_raw.stem}'
make_dir(path_export_inference)
path_export = path / 'export'
file_csv = path_export / f'pred_{file_raw.stem}.csv'

path_model = path / 'training_data/model_multi_labels_all/vietnamese-bi-encoder/2024-11-15 13:29:02'

api_endpoint = 'https://datasuite.shopee.io/datahub/api/v1/usertoken/upload/csv/csv-88614dc5-d1d4-4b24-afde-01157ae79875'
ingestion_token = '507878de-8603-448f-b2bc-d1113b158655'

# data
query = f"""
select * exclude(comment_star)
, cast(unnest(comment_star, recursive := true)::json as STRUCT(comment_id bigint, comment VARCHAR, rating_star int)) comment_star
from read_parquet('{file_raw}')
"""
df = (
    duckdb.sql(query).pl()
    .unnest('comment_star')
    .with_row_index('index')
)
print(
    f'Data Shape: {df.shape} '
    f'Items: {df['item_id'].n_unique()}'
)

# inference
col = ['index', 'comment_id', 'comment']
infer = InferenceTextClassification(
    path_model=str(path_model),
    col='comment',
    torch_compile=True,
    fp16=True
)

# batching
batches, num_batches = data_batching(df.shape[0], n_size=100_000)
for i, v in batches.items():
    file_export = path_export_inference / f'{file_raw.stem}_{i}.parquet'
    if file_export.exists():
        print(f'Batch Done: {file_export.stem}')
        continue

    # infer
    print(f'Start Batch {i}/{num_batches}: {file_export.stem}')
    ds_pred = infer.run(data=df[col].filter(pl.col('index').is_in(v)))

    # post process
    ds_pred_post = (
        ds_pred
        .to_polars()
        .explode(['labels', 'score'])
        .pivot(index=col, on='labels', values='score', aggregate_function='sum')
     )

    # export
    ds_pred_post.write_parquet(path_export_inference / f'{file_raw.stem}_{i}.parquet')


# concat on files
query = f"""select * from read_parquet('{path_export_inference}/*.parquet')"""
tmp = duckdb.sql(query).pl()
print(f'Data Inference shape: {tmp.shape}')

df_export = (
    df.join(tmp.drop(['comment']), how='left', on='comment_id', coalesce=True)
    .select(df.columns + infer.id2label)
    .drop(['index'])
)
print(f'Data merge Inference shape: {df_export.shape}')

# up to data hub
df_export.write_csv(file_csv)
upload_to_datahub(file_csv, api_endpoint, ingestion_token)
