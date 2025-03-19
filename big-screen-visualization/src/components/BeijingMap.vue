<template>
  <div class="map-container" ref="mapContainer"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  odData: {
    type: Array,
    default: () => []
  }
});

const mapContainer = ref(null);
let map = null;

onMounted(() => {
  console.log('初始化地图组件');
  // 初始化地图，设置中心点为北京市中心
  map = new T.Map(mapContainer.value);
  map.centerAndZoom(new T.LngLat(116.404, 39.915), 12); // 放大地图级别到12
  
  // 添加控件
  map.addControl(new T.Control.Zoom()); // 缩放控件
  map.addControl(new T.Control.Scale()); // 比例尺控件
  map.addControl(new T.Control.MapType()); // 地图类型控件
});

// 监听OD数据变化
watch(() => props.odData, (newData) => {
  console.log('地图组件接收到OD数据:', newData?.length);
  if (newData && newData.length > 0) {
    // 检查第一项数据的结构
    console.log('OD数据第一项:', JSON.stringify(newData[0]._source));
    updateMapWithOdData(newData);
  } else {
    console.log('未接收到有效OD数据');
    // 清除现有覆盖物
    if (map) map.clearOverLays();
  }
}, { deep: true });

// 更新地图OD数据
const updateMapWithOdData = (data) => {
  // 确保地图已初始化
  if (!map) {
    console.error('地图尚未初始化');
    return;
  }
  
  console.log(`准备在地图上展示${data.length}条数据`);
  
  // 清除现有覆盖物
  map.clearOverLays();
  
  // 为不同的OD线路使用不同颜色
  const colors = ['#1a73e8', '#ff7043', '#00c853', '#aa00ff', '#ffab00'];
  
  let successCount = 0;
  let errorCount = 0;
  
  // 添加OD数据到地图
  data.forEach((item, index) => {
    // 获取ES返回的_source数据
    const source = item._source;
    if (!source) {
      console.error('数据项缺少_source字段:', item);
      errorCount++;
      return;
    }
    
    // 检查必要的字段是否存在
    if (!source.O_point || !source.D_point) {
      console.error('数据缺少必要的坐标字段:', source);
      errorCount++;
      return;
    }
    
    // 获取OD坐标 - 从嵌套对象中获取
    try {
      // 确保经纬度都是数字
      const oLon = Number(source.O_point.lon);
      const oLat = Number(source.O_point.lat);
      const dLon = Number(source.D_point.lon);
      const dLat = Number(source.D_point.lat);
      
      // 创建天地图坐标点
      const originPoint = new T.LngLat(oLon, oLat);
      const destPoint = new T.LngLat(dLon, dLat);
      
      // 随机选择颜色
      const color = colors[index % colors.length];
      
      // 创建起点标记 - 使用默认标记
      const originMarker = new T.Marker(originPoint);
      map.addOverLay(originMarker);
      
      // 创建终点标记 - 使用默认标记  
      const destMarker = new T.Marker(destPoint);
      map.addOverLay(destMarker);
      
      // 创建连线
      const line = new T.Polyline([originPoint, destPoint], {
        color: color,
        weight: 3,
        opacity: 0.8
      });
      map.addOverLay(line);
      
      successCount++;
    } catch (error) {
      console.error(`添加地图元素失败(数据索引${index}):`, error);
      console.error('问题数据:', JSON.stringify(source));
      errorCount++;
    }
  });
  
  console.log(`成功绘制了${successCount}条OD线路，失败${errorCount}条，总数据${data.length}条`);
  
  // 如果成功添加了一些数据，调整地图视野以包含所有数据
  if (successCount > 0) {
    try {
      // 创建边界对象
      const bounds = map.getViewport(map.getOverlays());
      // 调整地图视野
      map.setViewport(bounds);
    } catch (e) {
      console.error('设置地图视野失败:', e);
    }
  }
};
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid rgba(0, 180, 255, 0.5);
}
</style>