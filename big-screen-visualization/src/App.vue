<script setup>
import { ref, onMounted } from 'vue';
import BeijingMap from './components/BeijingMap.vue';
import PieChart from './components/PieChart.vue';
import BarChart from './components/BarChart.vue';
import LineChart from './components/LineChart.vue';
import DataTable from './components/DataTable.vue';
import GaugeChart from './components/GaugeChart.vue';

// 当前时间
const currentTime = ref(new Date().toLocaleString());

// 更新时间
onMounted(() => {
  setInterval(() => {
    currentTime.value = new Date().toLocaleString();
  }, 1000);
});
</script>

<template>
  <div class="dashboard">
    <!-- 头部 -->
    <div class="header">
      <div class="title">数据可视化系统</div>
      <div class="time">{{ currentTime }}</div>
    </div>
    
    <!-- 内容区域 -->
    <div class="content">
      <!-- 左侧面板 -->
      <div class="left-panel">
        <div class="panel-item">
          <PieChart />
        </div>
        <div class="panel-item">
          <GaugeChart />
        </div>
        <div class="panel-item">
          <DataTable />
        </div>
      </div>
      
      <!-- 中间地图 -->
      <div class="center-panel">
        <BeijingMap />
      </div>
      
      <!-- 右侧面板 -->
      <div class="right-panel">
        <div class="panel-item">
          <BarChart />
        </div>
        <div class="panel-item">
          <LineChart />
        </div>
      </div>
    </div>
    
    <!-- 底部面板 -->
    <div class="bottom-panel">
      <div class="panel-item">
        <LineChart />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

.header {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background: linear-gradient(to right, rgba(0, 180, 255, 0.1), rgba(0, 180, 255, 0.3), rgba(0, 180, 255, 0.1));
  border: 1px solid rgba(0, 180, 255, 0.5);
  border-radius: 4px;
  margin-bottom: 10px;
  flex-shrink: 0;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
  letter-spacing: 2px;
}

.time {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
}

.content {
  flex: 1;
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  min-height: 0; /* 确保flex子元素不会溢出 */
}

.left-panel, .right-panel {
  width: 25%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 0; /* 确保flex子元素不会溢出 */
}

.center-panel {
  flex: 1;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  min-height: 0; /* 确保flex子元素不会溢出 */
}

.bottom-panel {
  height: 20%;
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.panel-item {
  flex: 1;
  background-color: rgba(0, 180, 255, 0.05);
  border: 1px solid rgba(0, 180, 255, 0.5);
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0; /* 确保flex子元素不会溢出 */
}

.panel-title {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
  letter-spacing: 2px;
}

@media (max-width: 768px) {
  .content {
    flex-direction: column;
  }
  
  .left-panel, .right-panel {
    width: 100%;
    height: auto;
  }
  
  .bottom-panel {
    height: auto;
  }
}
</style>
