const express = require('express');
const { Client } = require('@elastic/elasticsearch');
const cors = require('cors');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// 中间件
app.use(cors());
app.use(express.json());

// 创建Elasticsearch客户端连接
const client = new Client({
  node: process.env.ELASTICSEARCH_URL || 'http://localhost:9200',
  auth: {
    username: process.env.ELASTICSEARCH_USERNAME || 'elastic',
    password: process.env.ELASTICSEARCH_PASSWORD || '-KFLCdZa6PH6gnin6i_b'
  }
});

// 测试连接
app.get('/api/health', async (req, res) => {
  try {
    const info = await client.info();
    res.json({
      status: 'OK',
      elasticsearchInfo: info
    });
  } catch (error) {
    console.error('Elasticsearch连接错误:', error);
    res.status(500).json({ error: '无法连接到Elasticsearch' });
  }
});

// 按时间查询OD数据
app.get('/api/od_data', async (req, res) => {
  try {
    const { date, hour } = req.query;
    let query = { match_all: {} };
    
    // 构建查询条件
    if (date || hour) {
      if (date && hour) {
        // 格式化日期：从YYYY-MM-DD转为YYYYMMDD
        const formattedDate = date.replace(/-/g, '');
        const hourNum = parseInt(hour);
        const hourStr = hourNum.toString().padStart(2, '0');
        
        // 构建ES期望的格式：yyyyMMdd HHmmss
        const startTimeStr = `${formattedDate} ${hourStr}0000`;
        const endTimeStr = `${formattedDate} ${hourStr}5959`;
        
        query = {
          range: {
            O_time: {
              gte: startTimeStr,
              lte: endTimeStr
            }
          }
        };
        
        console.log(`查询时间范围: ${startTimeStr} 到 ${endTimeStr}`);
      } else if (date) {
        // 只有日期，查询整天
        const formattedDate = date.replace(/-/g, '');
        
        // 构建ES期望的格式：yyyyMMdd HHmmss
        const startTimeStr = `${formattedDate} 000000`;
        const endTimeStr = `${formattedDate} 235959`;
        
        query = {
          range: {
            O_time: {
              gte: startTimeStr,
              lte: endTimeStr
            }
          }
        };
        
        console.log(`查询日期: ${formattedDate} (全天)`);
      } else if (hour) {
        // 只有小时，查询所有日期中的该小时
        const hourNum = parseInt(hour);
        const hourStr = hourNum.toString().padStart(2, '0');
        
        // 使用前缀查询所有以指定小时开头的时间
        query = {
          wildcard: {
            O_time: `* ${hourStr}*`
          }
        };
        
        console.log(`查询所有日期中${hourStr}时的数据`);
      }
    }
    
    console.log("执行ES查询:", JSON.stringify(query));
    
    const result = await client.search({
      index: 'taxi_od',
      body: {
        query: query,
        size: 100  // 限制返回数量
      }
    });
    
    // 处理响应
    let hits = [];
    if (result && result.body && result.body.hits) {
      hits = result.body.hits.hits || [];
    } else if (result && result.hits) {
      hits = result.hits.hits || [];
    }
    
    console.log(`查询返回${hits.length}条结果`);
    
    // 添加调试信息查看第一条数据结构
    if (hits.length > 0) {
      console.log('数据结构示例:', JSON.stringify(hits[0]._source).substring(0, 200));
    }
    
    res.json(hits);
  } catch (error) {
    console.error('查询OD数据错误:', error);
    res.status(500).json({ error: '查询OD数据失败: ' + error.message });
  }
});

// 启动服务器
app.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});