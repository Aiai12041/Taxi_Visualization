<template>
  <div class="table-container">
    <div class="table-header">
      <div class="header-item">人员</div>
      <div class="header-item">月均量</div>
      <div class="header-item">月环比</div>
    </div>
    <div class="table-body">
      <div class="table-row" v-for="(item, index) in tableData" :key="index">
        <div class="table-cell">{{ item.name }}</div>
        <div class="table-cell">{{ item.value }}</div>
        <div class="table-cell">{{ item.rate }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 模拟数据
const tableData = ref([
  { name: '张三', value: '12508', rate: '89%' },
  { name: '李四', value: '16930', rate: '93%' },
  { name: '王五', value: '15927', rate: '91%' },
  { name: '赵六', value: '15721', rate: '90%' },
  { name: '钱七', value: '18430', rate: '95%' }
]);
</script>

<style scoped>
.table-container {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid rgba(0, 180, 255, 0.5);
  color: #fff;
}

.table-header {
  display: flex;
  background-color: rgba(0, 180, 255, 0.2);
  padding: 10px 0;
}

.header-item {
  flex: 1;
  text-align: center;
  font-weight: bold;
}

.table-body {
  height: calc(100% - 40px);
  overflow-y: auto;
}

.table-row {
  display: flex;
  padding: 10px 0;
  border-bottom: 1px solid rgba(0, 180, 255, 0.2);
}

.table-row:nth-child(odd) {
  background-color: rgba(0, 180, 255, 0.1);
}

.table-cell {
  flex: 1;
  text-align: center;
}
</style>