<template>
  <div class="chart-container" ref="chartContainer"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

const chartContainer = ref(null);
let chart = null;

onMounted(() => {
  // 初始化图表
  chart = echarts.init(chartContainer.value);
  
  // 随机生成数据
  const dates = ['11-01', '11-02', '11-03', '11-04', '11-05', '11-06', '11-07', '11-08', '11-09', '11-10', 
                '11-11', '11-12', '11-13', '11-14', '11-15'];
  const data1 = dates.map(() => Math.floor(Math.random() * 150) + 50);
  const data2 = dates.map(() => Math.floor(Math.random() * 200) + 100);
  
  // 设置图表选项
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'line'
      }
    },
    legend: {
      data: ['指标1', '指标2'],
      textStyle: {
        color: '#fff'
      },
      top: 0,
      right: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates,
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        }
      },
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.7)'
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      },
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.7)'
      }
    },
    series: [
      {
        name: '指标1',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        itemStyle: {
          color: '#00f0ff'
        },
        lineStyle: {
          width: 2,
          color: '#00f0ff'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(0, 240, 255, 0.3)' },
            { offset: 1, color: 'rgba(0, 240, 255, 0)' }
          ])
        },
        data: data1
      },
      {
        name: '指标2',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        itemStyle: {
          color: '#ff88eb'
        },
        lineStyle: {
          width: 2,
          color: '#ff88eb'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 136, 235, 0.3)' },
            { offset: 1, color: 'rgba(255, 136, 235, 0)' }
          ])
        },
        data: data2
      }
    ]
  };
  
  // 应用配置项
  chart.setOption(option);
  
  // 响应窗口大小变化
  window.addEventListener('resize', handleResize);
});

// 处理窗口大小变化
const handleResize = () => {
  chart && chart.resize();
};

onUnmounted(() => {
  // 移除事件监听器
  window.removeEventListener('resize', handleResize);
  // 销毁图表实例
  chart && chart.dispose();
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid rgba(0, 180, 255, 0.5);
}
</style>