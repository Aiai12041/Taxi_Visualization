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
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
  const data1 = months.map(() => Math.floor(Math.random() * 200) + 50);
  const data2 = months.map(() => Math.floor(Math.random() * 300) + 100);
  
  // 设置图表选项
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['数据1', '数据2'],
      textStyle: {
        color: '#fff'
      },
      top: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: months,
        axisLine: {
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.3)'
          }
        },
        axisLabel: {
          color: 'rgba(255, 255, 255, 0.7)'
        }
      }
    ],
    yAxis: [
      {
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
      }
    ],
    series: [
      {
        name: '数据1',
        type: 'bar',
        stack: 'Ad',
        emphasis: {
          focus: 'series'
        },
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        },
        data: data1
      },
      {
        name: '数据2',
        type: 'bar',
        stack: 'Ad',
        emphasis: {
          focus: 'series'
        },
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#ea8cff' },
            { offset: 0.5, color: '#9a36ff' },
            { offset: 1, color: '#9a36ff' }
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