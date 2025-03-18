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
  
  // 设置图表选项
  const option = {
    backgroundColor: 'transparent',
    series: [{
      type: 'gauge',
      radius: '90%',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: 100,
      splitNumber: 10,
      axisLine: {
        lineStyle: {
          width: 6,
          color: [
            [0.3, '#67e0e3'],
            [0.7, '#37a2da'],
            [1, '#fd666d']
          ]
        }
      },
      pointer: {
        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
        length: '12%',
        width: 20,
        offsetCenter: [0, '-60%'],
        itemStyle: {
          color: 'auto'
        }
      },
      axisTick: {
        length: 12,
        lineStyle: {
          color: 'auto',
          width: 2
        }
      },
      splitLine: {
        length: 20,
        lineStyle: {
          color: 'auto',
          width: 5
        }
      },
      axisLabel: {
        color: '#fff',
        fontSize: 16,
        distance: -60,
        formatter: function(value) {
          if (value === 100) {
            return '100%';
          } else if (value === 0) {
            return '0%';
          }
          return '';
        }
      },
      title: {
        offsetCenter: [0, '-20%'],
        fontSize: 20,
        color: '#fff'
      },
      detail: {
        fontSize: 30,
        offsetCenter: [0, '0%'],
        valueAnimation: true,
        formatter: function(value) {
          return Math.round(value) + '%';
        },
        color: '#fff'
      },
      data: [{
        value: 70,
        name: '完成率'
      }]
    }]
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