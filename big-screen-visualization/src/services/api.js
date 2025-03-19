import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  withCredentials: false,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
});

export default {
  // 检查ES健康状态
  getHealth() {
    return apiClient.get('/health');
  },
  
  // 获取数据示例
  getData() {
    return apiClient.get('/data');
  },

  // 获取特定日期/小时的OD数据
  getOdData(date, hour) {
    return apiClient.get('/od_data', {
      params: { date, hour }
    });
  },
  
  // 可以添加更多特定的API调用方法
}