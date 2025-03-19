<script setup>
import { ref, onMounted } from 'vue';
import BeijingMap from './components/BeijingMap.vue';
import PieChart from './components/PieChart.vue';
import BarChart from './components/BarChart.vue';
import LineChart from './components/LineChart.vue';
import DataTable from './components/DataTable.vue';
import GaugeChart from './components/GaugeChart.vue';
import ApiService from './services/api.js';  // 导入API服务

// 当前时间
const currentTime = ref(new Date().toLocaleString());
// API数据和状态
const esStatus = ref('未连接');
const apiData = ref([]);
const loading = ref(false);
const error = ref(null);
// 添加日期和时间选择器状态
const selectedDate = ref('');
const selectedHour = ref('');
const odData = ref([]);

// 更新时间
onMounted(() => {
  setInterval(() => {
    currentTime.value = new Date().toLocaleString();
  }, 1000);
   // 获取API数据
   fetchApiData();
});

// 获取API数据的函数
const fetchApiData = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // 获取ES健康状态
    const healthResponse = await ApiService.getHealth();
    esStatus.value = healthResponse.data.status;
    
    // 获取数据
    const dataResponse = await ApiService.getData();
    apiData.value = dataResponse.data;
  } catch (err) {
    console.error('API请求失败:', err);
    error.value = '无法连接到服务器或数据获取失败';
  } finally {
    loading.value = false;
  }
};

// 刷新API数据
const refreshData = () => {
  fetchApiData();
};

// 获取OD数据的函数
const fetchOdData = async () => {
  if (!selectedDate.value && !selectedHour.value) {
    console.log('未选择日期或小时，跳过查询');
    return;
  }
  
  loading.value = true;
  error.value = null;
  console.log(`请求OD数据: 日期=${selectedDate.value}, 小时=${selectedHour.value}`);
  
  try {
    const response = await ApiService.getOdData(selectedDate.value, selectedHour.value);
    console.log(`获取到${response.data.length}条OD数据`);
    
    if (response.data.length > 0) {
      // 检查第一条数据
      console.log('第一条数据样本:', JSON.stringify(response.data[0]._source));
    }
    
    odData.value = response.data;
  } catch (err) {
    console.error('获取OD数据失败:', err);
    error.value = '无法获取OD数据: ' + (err.message || JSON.stringify(err));
  } finally {
    loading.value = false;
  }
};
// 处理日期或时间变化
const handleDateTimeChange = () => {
  console.log('选择的日期:', selectedDate.value);
  console.log('选择的小时:', selectedHour.value);
  console.log('小时值类型:', typeof selectedHour.value);
  fetchOdData();
};

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
          <!-- API结果显示框 -->
          <div class="api-result-box">
            <div class="api-result-header">
              <h3>ES数据查询结果</h3>
              <button @click="refreshData" class="refresh-btn" :disabled="loading">
                {{ loading ? '加载中...' : '刷新' }}
              </button>
            </div>
            <div class="api-result-content">
              <div v-if="loading" class="loading">加载中...</div>
              <div v-else-if="error" class="error">{{ error }}</div>
              <div v-else>
                <div class="status-row">
                  <span class="status-label">ES状态:</span>
                  <span class="status-value" :class="{ 'status-ok': esStatus === 'OK' }">{{ esStatus }}</span>
                </div>
                <div v-if="apiData.length > 0" class="data-preview">
                  <div v-for="(item, index) in apiData.slice(0, 5)" :key="index" class="data-item">
                    {{ JSON.stringify(item._source || item).slice(0, 50) }}{{ JSON.stringify(item._source || item).length > 50 ? '...' : '' }}
                  </div>
                  <div v-if="apiData.length > 5" class="more-data">
                    还有{{ apiData.length - 5 }}条数据...
                  </div>
                </div>
                <div v-else class="no-data">
                  暂无数据
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 中间地图 -->
      <div class="center-panel">
      <div class="map-filter">
        <h3>OD数据筛选</h3>
        <div class="filter-controls">
          <el-date-picker
            v-model="selectedDate"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleDateTimeChange"
          ></el-date-picker>
          <el-select 
            v-model="selectedHour" 
            placeholder="选择小时"
            @change="handleDateTimeChange"
            class="hour-select"
          >
            <el-option 
              v-for="i in 24" 
              :key="i-1" 
              :label="`${i-1}时`" 
              :value="(i-1).toString().padStart(2, '0')" 
            ></el-option>
          </el-select>
        </div>
      </div>
      <BeijingMap :od-data="odData" />
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

.map-filter {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 1000;
  background: rgba(0, 23, 51, 0.8);
  padding: 10px;
  border-radius: 4px;
  border: 1px solid rgba(0, 180, 255, 0.5);
  color: #fff;
}

.filter-controls {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.hour-select {
  width: 120px;
}

/* API结果框样式 */
.api-result-box {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 10px;
}

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
