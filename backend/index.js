require('dotenv').config();
const express = require('express');
const cors = require('cors');
const userRoutes = require('./routes/userRoutes');

// Express 앱 생성

const app = express();
const PORT = process.env.PORT || 3000;

// 미들웨어 설정
app.use(cors());
app.use(express.json()); // JSON 요청 처리
app.use(express.urlencoded({ extended: true })); // URL 인코딩된 데이터 처리

// 기본 라우트
app.get('/', (req, res) => {
  res.send('Backend Server is Running!');
});

// 서버 실행
app.listen(PORT, () => {
  console.log(`🚀 Server is running on http://localhost:${PORT}`);
});

app.use('/users', userRoutes);