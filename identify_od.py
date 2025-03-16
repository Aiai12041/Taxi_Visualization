import pandas as pd
from collections import defaultdict
import geopandas as gpd
from shapely.geometry import Point
import json

# --------------------- 第一阶段：OD点识别（流式处理） ---------------------
def process_large_txt(input_path, output_od_path):
    """流式处理原始TXT，识别OD点"""
    # 使用字典跟踪每辆车的最新状态
    car_status = defaultdict(lambda: {'last_status': None, 'o_point': None, 'o_time': None})
    
    with open(input_path, 'r', encoding='utf-8') as f_in, \
         open(output_od_path, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:  # 逐行读取
            records = line.strip().split(';')
            for record in records:
                if not record:
                    continue  # 跳过空记录
                
                fields = record.strip().split(',')
                if len(fields) < 11:
                    continue  # 跳过字段数不足的记录
                
                # 数据类型转换（减少内存占用）
                date = fields[0]
                time = fields[1]
                car_id = fields[3]
                lng = float(fields[4])
                lat = float(fields[5])
                status = int(fields[8])
                timestamp = f"{date}T{time}"  # 合并为ISO格式
                
                # 状态变化检测
                last = car_status[car_id]
                if last['last_status'] == 0 and status == 1:  # 上车事件
                    last.update({
                        'o_time': timestamp,
                        'o_point': (lng, lat),
                        'last_status': status
                    })
                elif last['last_status'] == 1 and status == 0:  # 下车事件
                    if last['o_point']:  # 确保有对应的上车点
                        od_record = {
                            "车ID": car_id,
                            "O_time": last['o_time'],
                            "O_lng": last['o_point'][0],
                            "O_lat": last['o_point'][1],
                            "D_time": timestamp,
                            "D_lng": lng,
                            "D_lat": lat
                        }
                        f_out.write(json.dumps(od_record) + '\n')  # 立即写入磁盘
                        last.update({'o_point': None})  # 重置上车点
                    last['last_status'] = status
                else:
                    last['last_status'] = status

# --------------------- 第二阶段：关联POI（分块处理） ---------------------
def add_poi_info(od_path, poi_shp_path, output_final_path, chunk_size=10000):
    """分块处理OD数据并关联POI"""
    # 加载POI数据并构建空间索引
    poi_gdf = gpd.read_file(poi_shp_path)
    poi_gdf = poi_gdf.to_crs("EPSG:3857")  # 转换为投影坐标系
    poi_gdf['geometry'] = poi_gdf.geometry.buffer(10)  # 创建微小缓冲提高匹配成功率
    
    # 分块读取OD数据
    chunk_iter = pd.read_json(od_path, lines=True, chunksize=chunk_size)
    
    for i, chunk in enumerate(chunk_iter):
        # 转换为GeoDataFrame
        gdf = gpd.GeoDataFrame(
            chunk,
            geometry=[Point(xy) for xy in zip(chunk['O_lng'], chunk['O_lat'])]
        ).set_crs("EPSG:4326").to_crs("EPSG:3857")
        
        # 空间连接（最近邻匹配）
        merged = gpd.sjoin_nearest(gdf, poi_gdf, how='left', max_distance=1000)  # 约5公里
        
        # 检查是否存在'name'列
        if 'name' not in merged.columns:
            merged['name'] = None  # 如果不存在，添加一个空的'name'列

        # 保存结果（追加模式）
        merged[['车ID', 'O_time', 'O_lng', 'O_lat', 'D_time', 'D_lng', 'D_lat', 'name']] \
            .to_csv(output_final_path, mode='a' if i>0 else 'w', index=False, header=(i==0))

# --------------------- 执行流程 ---------------------
if __name__ == "__main__":
    # 第一步：提取OD点（流式处理）
    process_large_txt("./20171204_001.txt", "temp_od.jsonl")
    
    # 第二步：关联POI（分块处理）
    add_poi_info("temp_od.jsonl", "./poi.shp", "final_od.csv")
    
    # 第三步：清理临时文件（可选）
    import os; os.remove("temp_od.jsonl")