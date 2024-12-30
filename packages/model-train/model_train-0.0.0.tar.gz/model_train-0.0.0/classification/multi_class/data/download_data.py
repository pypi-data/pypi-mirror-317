from core_pro import DataPipeLine

query = open('query.sql')
df = DataPipeLine(query).run_presto_to_df(save_path=path / 'raw/raw_star_above_3_2024_11_12.parquet')
