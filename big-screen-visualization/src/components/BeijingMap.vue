<template>
  <div class="map-container" ref="mapContainer"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const mapContainer = ref(null);

onMounted(() => {
  // 初始化地图，设置中心点为北京市中心
  const map = new T.Map(mapContainer.value);
  map.centerAndZoom(new T.LngLat(116.404, 39.915), 10);
  
  // 添加控件
  map.addControl(new T.Control.Zoom()); // 缩放控件
  map.addControl(new T.Control.Scale()); // 比例尺控件
  map.addControl(new T.Control.MapType()); // 地图类型控件
  
  // 添加一些标记点，模拟数据点
  const markers = [
    { lng: 116.404, lat: 39.915, name: '北京市中心' },
    { lng: 116.310, lat: 39.990, name: '海淀区' },
    { lng: 116.432, lat: 39.910, name: '朝阳区' },
    { lng: 116.280, lat: 39.865, name: '丰台区' },
    { lng: 116.588, lat: 39.809, name: '通州区' },
    { lng: 116.225, lat: 40.220, name: '昌平区' },
  ];
  
  // 创建连线，模拟数据流动
  markers.forEach((marker, index) => {
    // 创建标记
    const markerObj = new T.Marker(new T.LngLat(marker.lng, marker.lat));
    map.addOverLay(markerObj);
    
    // 创建标签
    const label = new T.Label({
      text: marker.name,
      position: new T.LngLat(marker.lng, marker.lat),
      offset: new T.Point(-20, -10)
    });
    map.addOverLay(label);
    
    // 创建与中心点的连线
    if (index > 0) {
      const line = new T.Polyline([
        new T.LngLat(116.404, 39.915),
        new T.LngLat(marker.lng, marker.lat)
      ], {
        color: '#00f',
        weight: 2,
        opacity: 0.6
      });
      map.addOverLay(line);
    }
  });
});
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