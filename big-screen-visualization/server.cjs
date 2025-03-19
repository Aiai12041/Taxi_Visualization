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

// 获取数据示例
app.get('/api/data', async (req, res) => {
  try {
    const result = await client.search({
      index: 'taxi_od',
      body: {
        query: {
          match_all: {}
        },
        size: 10
      }
    });

    // 更安全地处理响应结构
    console.log('ES搜索结果结构:', JSON.stringify(result, null, 2));
    
    // 尝试不同可能的响应结构
    let hits = [];
    if (result && result.body && result.body.hits) {
      hits = result.body.hits.hits || [];
    } else if (result && result.hits) {
      hits = result.hits.hits || [];
    }
    
    res.json(hits);
  } catch (error) {
    console.error('查询错误:', error);
    res.status(500).json({ error: '查询数据失败' });
  }
});

// 启动服务器
app.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});