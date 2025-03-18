import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// 引入Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 引入ECharts
import * as echarts from 'echarts'

const app = createApp(App)

// 全局挂载echarts
app.config.globalProperties.$echarts = echarts

app.use(ElementPlus)
app.mount('#app')
