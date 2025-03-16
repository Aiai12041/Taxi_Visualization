import os
import json

def txt_to_json(txt_file_path, json_file_path):
    data = []
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split(',')
            record = {
                "年月日": fields[0],
                "时分秒": fields[1],
                "公司代码": fields[2],
                "车ID": fields[3],
                "经度": fields[4],
                "纬度": fields[5],
                "瞬时速度": fields[6],
                "方向角": fields[7],
                "空重状态": fields[8],
                "设备状态": fields[9],
                "接收时间": fields[10]
            }
            data.append(record)
    
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def process_folder(input_folder_path, output_folder_path):
    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            if file.endswith('.txt'):
                txt_file_path = os.path.join(root, file)
                json_file_name = os.path.splitext(file)[0] + '.json'
                json_file_path = os.path.join(output_folder_path, json_file_name)
                txt_to_json(txt_file_path, json_file_path)
                print(f"Converted {txt_file_path} to {json_file_path}")

if __name__ == "__main__":
    input_folder_path = input("请输入要处理的文件夹路径: ")
    output_folder_path = input("请输入输出文件夹路径: ")
    process_folder(input_folder_path, output_folder_path)