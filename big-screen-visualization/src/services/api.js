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
  
  // 可以添加更多特定的API调用方法
}