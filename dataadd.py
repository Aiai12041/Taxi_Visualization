from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "-KFLCdZa6PH6gnin6i_b"),  # 必填项
    verify_certs=False,  # 禁用证书验证（开发环境）
    request_timeout=60
)

CHUNK_SIZE = 5000

def gen_actions(file_path):
    for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):
        for _, row in chunk.iterrows():
            yield {
                "_index": "taxi_od",
                "_source": {
                    "车ID": str(row["车ID"]),
                    "O_time": f"{row['O_time']}",  # 确保时间格式正确
                    "O_point": f"{row['O_lng']},{row['O_lat']}",
                    "D_point": f"{row['D_lng']},{row['D_lat']}",
                    "POI_name": row.get("name", "")
                }
            }

def bulk_import(file_path):
    try:
        success, errors = helpers.bulk(
            client=es,
            actions=gen_actions(file_path),
            stats_only=False
        )
        print(f"成功导入: {success}")
        if errors:
            print(f"失败记录: {len(errors)}")
            with open("error_log.json", "w") as f:
                json.dump(errors, f)
    except Exception as e:
        print(f"严重错误: {str(e)}")

if __name__ == "__main__":
    bulk_import("final_od.csv")
