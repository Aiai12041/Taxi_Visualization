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
  const data = [
    { value: 10, name: 'data1' },
    { value: 15, name: 'data2' },
    { value: 25, name: 'data3' },
    { value: 20, name: 'data4' },
    { value: 30, name: 'data5' },
    { value: 5, name: 'data6' }
  ];
  
  // 设置图表选项
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 10,
      top: 'center',
      textStyle: {
        color: '#fff'
      }
    },
    series: [
      {
        name: '数据分布',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#0a1a35',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold',
            color: '#fff'
          }
        },
        labelLine: {
          show: false
        },
        data: data
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