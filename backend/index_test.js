require('dotenv').config();
const express = require('express');
const mysql = require('./src/database/index');  // MySQL 연결
const mongoose = require('./src/database/mongodb');  // MongoDB 연결
const cors = require('cors'); 
const app = express();
const port = process.env.PORT || 3000;
const router = require('./src/router');
const bodyParser = require('body-parser');
const mongoRoutes = require('./routes/mongoRoute');  // 추가

app.use(cors());

 
// JSON 형식의 데이터 처리
app.use(bodyParser.json());
// URL 인코딩 된 데이터 처리
app.use(bodyParser.urlencoded({ extended: true }));

// 라우터를 애플리케이션에 등록
app.use('/', router);



// 테스트 API: MySQL 연결 확인
app.get('/mysql-test', async (req, res) => {
  try {
    const [rows] = await mysql.query('SELECT 1 + 1 AS result');
    res.json({ message: '✅ MySQL 연결 성공', data: rows });
  } catch (err) {
    res.status(500).json({ message: '❌ MySQL 연결 실패', error: err });
  }
});

// 테스트 API: MongoDB 연결 확인
app.get('/mongo-test', async (req, res) => {
  try {
    const collections = await mongoose.connection.db.listCollections().toArray();
    res.json({ message: '✅ MongoDB 연결 성공', collections });
  } catch (err) {
    res.status(500).json({ message: '❌ MongoDB 연결 실패', error: err });
  }
});
app.use('/api', mongoRoutes);


// 서버 실행
app.listen(port, () => {
  console.log(`🚀 서버가 ${port}번 포트에서 실행 중...`);
});
