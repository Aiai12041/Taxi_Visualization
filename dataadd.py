from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json
import traceback
import sys

print("开始执行脚本...")

# 创建连接
print("尝试连接Elasticsearch...")
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "-KFLCdZa6PH6gnin6i_b"),  # 必填项
    verify_certs=False,  # 禁用证书验证（开发环境）
    request_timeout=60
)

if es.ping():
    print('连接成功')
    print(f"Elasticsearch版本: {es.info()['version']['number']}")
else:
    print('连接失败')
    sys.exit(1)

# 检查索引映射
try:
    if es.indices.exists(index="taxi_od"):
        print("索引taxi_od已存在，当前映射:")
        print(es.indices.get_mapping(index="taxi_od"))
    else:
        print("索引taxi_od不存在，将在首次导入时创建")
except Exception as e:
    print(f"检查索引时出错: {str(e)}")

CHUNK_SIZE = 5000

def gen_actions(file_path):
    print(f"开始读取文件: {file_path}")
    try:
        # 先尝试读取文件头，检查字段是否存在
        print("检查CSV文件结构...")
        header = pd.read_csv(file_path, nrows=0)
        print(f"文件字段: {header.columns.tolist()}")
        required_fields = ["车ID", "O_time", "O_lng", "O_lat", "D_lng", "D_lat"]
        for field in required_fields:
            if field not in header.columns:
                print(f"警告: 缺少必要字段 '{field}'")
        
        chunk_count = 0
        doc_count = 0
        error_count = 0
        
        # 分块处理文件
        for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):
            chunk_count += 1
            print(f"处理第{chunk_count}个数据块，包含{len(chunk)}条记录")
            
            for _, row in chunk.iterrows():
                doc_count += 1
                try:
                    # 转换为JSON文档
                    doc = {
                        "_index": "taxi_od",
                        "_source": {
                            "车ID": str(row["车ID"]),
                            "O_time": pd.to_datetime(row["O_time"]).strftime("%Y%m%d %H%M%S"),
                            "O_point": {  # 使用对象格式定义geo_point
                                "lon": float(row["O_lng"]),
                                "lat": float(row["O_lat"])
                            },
                            "D_point": {
                                "lon": float(row["D_lng"]),
                                "lat": float(row["D_lat"])
                            },
                            "POI_name": "unknown"
                        }
                    }
                    
                    # 每1000条打印一次
                    if doc_count % 1000 == 0:
                        print(f"已处理 {doc_count} 条记录")
                        
                    yield doc
                    
                except Exception as e:
                    error_count += 1
                    print(f"处理第{doc_count}条记录时出错: {str(e)}")
                    if error_count <= 5:  # 只显示前5条错误
                        print(f"问题数据: {row.to_dict()}")
                    
            print(f"完成块{chunk_count}处理，已处理{doc_count}条记录，错误{error_count}条")
            
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")
        print(traceback.format_exc())
        yield None  # 需要返回一个生成器

def bulk_import(file_path):
    print(f"开始导入数据到Elasticsearch...")
    try:
        # 计时开始
        import time
        start_time = time.time()
        
        # 执行批量导入
        print("执行批量导入操作...")
        success, errors = helpers.bulk(
            client=es,
            actions=gen_actions(file_path),
            stats_only=False,
            raise_on_error=False,  # 不要因单条错误停止整个过程
            chunk_size=CHUNK_SIZE  # 每次发送的批次大小
        )
        
        # 计算耗时
        elapsed_time = time.time() - start_time
        print(f"批量导入完成，耗时: {elapsed_time:.2f}秒")
        print(f"成功导入: {success}条记录")
        
        if errors:
            print(f"失败记录: {len(errors)}条")
            print("错误样本:")
            for i, error in enumerate(errors[:5]):  # 只显示前5条错误
                print(f"错误{i+1}: {error}")
            
            # 保存完整错误日志
            error_file = "error_log.json"
            print(f"将完整错误信息保存到: {error_file}")
            with open(error_file, "w") as f:
                json.dump(errors, f)
                
            # 分析错误类型
            error_types = {}
            for error in errors:
                error_type = error.get("index", {}).get("error", {}).get("type", "unknown")
                if error_type in error_types:
                    error_types[error_type] += 1
                else:
                    error_types[error_type] = 1
            
            print("错误类型统计:")
            for error_type, count in error_types.items():
                print(f"  - {error_type}: {count}条")
                
    except Exception as e:
        print(f"严重错误: {str(e)}")
        print("详细错误信息:")
        print(traceback.format_exc())

if __name__ == "__main__":
    file_path = "final_od.csv"
    print(f"准备处理文件: {file_path}")
    bulk_import(file_path)
    print("脚本执行完毕")