import pandas as pd
from collections import defaultdict
import geopandas as gpd
from shapely.geometry import Point
import json

# --------------------- 第一阶段：OD点识别（流式处理） ---------------------
def process_large_txt(input_path, output_od_path):
    """流式处理原始TXT，识别OD点"""
    car_status = defaultdict(lambda: {'last_status': None, 'o_point': None, 'o_time': None})
    od_count = 0
    status_stats = defaultdict(int)  # 状态统计

    with open(input_path, 'r', encoding='utf-8') as f_in, \
         open(output_od_path, 'w', encoding='utf-8') as f_out:

        for line_num, line in enumerate(f_in):
            records = line.strip().split(';')
            for record in records:
                if not record:
                    continue

                fields = record.split(',')
                if len(fields) < 11:
                    print(f"Line {line_num} 字段不足: {len(fields)}")
                    continue

                # === 调试：打印前3条数据样本 ===
                if line_num < 3:
                    print(f"[Debug] 样例数据: {fields}")

                try:
                    # === 关键字段索引修正 ===
                    date = fields[0]          # 年月日 (索引0)
                    time = fields[1]          # 时分秒 (索引1)
                    car_id = fields[3]        # 车ID (索引3)
                    lng = float(fields[4])    # 经度 (索引4)
                    lat = float(fields[5])    # 纬度 (索引5)
                    status = int(fields[8])   # 空重状态 (索引8)
                except (IndexError, ValueError) as e:
                    print(f"Line {line_num} 解析错误: {str(e)}")
                    continue

                # === 状态统计 ===
                status_stats[status] += 1

                # === 生成时间戳 ===
                timestamp = f"{date}T{time}"

                # === 状态机逻辑 ===
                last = car_status[car_id]
                
                # 规则：当状态从非载客（0/2/3）变为载客（1）时记录O点
                if status == 1 and last['last_status'] != 1:
                    last.update({
                        'o_time': timestamp,
                        'o_point': (lng, lat),
                        'last_status': 1
                    })
                    print(f"[Debug] 车辆 {car_id} 记录O点 @ {timestamp}")
                
                # 规则：当状态从载客（1）变为非载客（0/2/3）时记录D点
                elif last['last_status'] == 1 and status != 1:
                    if last['o_point']:
                        od_record = {
                            "车ID": car_id,
                            "O_time": last['o_time'],
                            "O_lng": last['o_point'][0],
                            "O_lat": last['o_point'][1],
                            "D_time": timestamp,
                            "D_lng": lng,
                            "D_lat": lat
                        }
                        f_out.write(json.dumps(od_record) + '\n')
                        od_count += 1
                        print(f"[Debug] 生成OD记录: {od_record}")
                    last.update({'o_point': None, 'last_status': status})
                
                # 其他情况只更新状态
                else:
                    last['last_status'] = status

        # === 输出统计信息 ===
        print("\n=== 状态统计 ===")
        print("空车(0):", status_stats.get(0, 0))
        print("载客(1):", status_stats.get(1, 0))
        print("停运(2):", status_stats.get(2, 0))
        print("异常(3):", status_stats.get(3, 0))
        print(f"\n生成的OD记录总数: {od_count}")

# --------------------- 第二阶段：关联POI（分块处理） ---------------------
def add_poi_info(od_path, poi_geojson_path, output_final_path, chunk_size=10000):
    # 读取POI数据并显式指定坐标系
    poi_gdf = gpd.read_file(poi_geojson_path)
    
    # 确保POI使用投影坐标系（假设x_display/y_display是投影坐标）
    poi_gdf = poi_gdf.set_geometry(
        gpd.points_from_xy(poi_gdf.DISPLAY_X, poi_gdf.DISPLAY_Y, crs="EPSG:3857")
    )
    
    # 分块处理OD数据
    chunk_iter = pd.read_json(od_path, lines=True, chunksize=chunk_size)
    
    for i, chunk in enumerate(chunk_iter):
        # 转换OD点坐标系到EPSG:3857
        gdf = gpd.GeoDataFrame(
            chunk,
            geometry=gpd.points_from_xy(
                chunk['O_lng'], 
                chunk['O_lat'], 
                crs="EPSG:4326"  # 原始数据是WGS84
            ).to_crs("EPSG:3857")  # 转换为投影坐标系
        )
        
        # 执行空间连接（确保坐标系一致）
        merged = gpd.sjoin_nearest(
            gdf, 
            poi_gdf, 
            how='left', 
            max_distance=500,  # 单位：米（适用于投影坐标系）
            distance_col='distance_to_poi'
        )
        # 保存结果（追加模式）
        merged[['车ID', 'O_time', 'O_lng', 'O_lat', 'D_time', 'D_lng', 'D_lat']] \
            .to_csv(output_final_path, mode='a' if i>0 else 'w', index=False, header=(i==0))

# --------------------- 执行流程 ---------------------
if __name__ == "__main__":
    # 第一步：提取OD点（流式处理）
    process_large_txt("./20171204_001.txt", "temp_od.jsonl")
    
    # 第二步：关联POI（分块处理）
    add_poi_info("temp_od.jsonl", "./poi_BJ.geojson", "final_od.csv")
    
    # 第三步：清理临时文件（可选）
    import os; os.remove("temp_od.jsonl")