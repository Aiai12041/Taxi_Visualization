import json
import os

def merge_json_files(input_folder_path, output_file_path, index_name):
    # 存储所有JSON文件的路径
    json_files = [os.path.join(input_folder_path, f) for f in os.listdir(input_folder_path) if f.endswith(".json")]

    # 打开一个文件用于写入Bulk数据
    with open(output_file_path, "w", encoding="utf-8") as bulk_file:
        for file in json_files:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 不指定 _id，让 Elasticsearch 自动生成
                bulk_file.write(json.dumps({"index": {"_index": index_name}}) + "\n")
                bulk_file.write(json.dumps(data) + "\n")

if __name__ == "__main__":
    input_folder_path = "E:/北京/20171204tr"  # 输入文件夹路径
    output_file_path = "E:/北京/bulk.json"  # 输出文件路径
    index_name = "vehicle_data"  # 设置Elasticsearch索引名称
    merge_json_files(input_folder_path, output_file_path, index_name)