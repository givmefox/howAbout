const express = require('express');
const router = express.Router();
const mongoose = require('../src/database/mongodb');  // MongoDB 연결 파일

// MongoDB users 컬렉션 모델 정의
const UserSchema = new mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,  // MongoDB ObjectId
  name: String,
  age: Number
});
const User = mongoose.model('User', UserSchema, 'users');  // 컬렉션명: users

// MongoDB 데이터 모델 (keyword_rank 컬렉션)
const KeywordSchema = new mongoose.Schema({
  순위: Number,
  키워드: String
});
const Keyword = mongoose.model('Keyword', KeywordSchema, 'keyword_rank'); //컬렉션명 : keyword_rank

// MongoDB 관련 키워드 컬렉션 모델 정의
const RelatedKeywordSchema = new mongoose.Schema({
  keyword: String,
  related: [String]
});
const RelatedKeyword = mongoose.model('RelatedKeyword', RelatedKeywordSchema, 'related_keywords');  // 컬렉션명: related_keywords

// MongoDB popular videos 컬렉션 모델 정의
const PopularVideoSchema = new mongoose.Schema({
  keyword: String,
  videos: [
    {
      video_id: String,
      score: Number
    }
  ]
});
const PopularVideo = mongoose.model('PopularVideo', PopularVideoSchema, 'keywords_popular_videos');  // 컬렉션명: keywords_popular_videos




// MongoDB에서 users 데이터 가져오기
router.get('/mongo-users', async (req, res) => {
  try {
    const users = await User.find();  // 모든 사용자 조회
    res.json({ message: '✅ MongoDB 데이터 조회 성공', data: users });
  } catch (error) {
    res.status(500).json({ message: '❌ MongoDB 데이터 조회 실패', error });
  }
});

// API 2: MongoDB에서 keyword_rank 데이터 가져오기 (순위별 정렬)
router.get('/mongo-rank', async (req, res) => {
  try {
    const keywords = await Keyword.find().sort({ 순위: 1 });  // 순위 오름차순 정렬
    res.json({ message: '✅ MongoDB keyword_rank 데이터 조회 성공', data: keywords });
  } catch (error) {
    res.status(500).json({ message: '❌ MongoDB keyword_rank 데이터 조회 실패', error });
  }
});


// 📌 API3: related_keywords 데이터 조회
router.get('/mongo-related-keywords', async (req, res) => {
  try {
    const keywords = await RelatedKeyword.find();  // 모든 데이터 조회
    res.json({ message: '✅ related_keywords 데이터 조회 성공', data: keywords });
  } catch (error) {
    res.status(500).json({ message: '❌ related_keywords 데이터 조회 실패', error });
  }
});

// 📌 API: keywords_popular_videos 데이터 조회
router.get('/mongo-popular-videos', async (req, res) => {
  try {
    const videos = await PopularVideo.find();  // 모든 데이터 조회
    res.json({ message: '✅ keywords_popular_videos 데이터 조회 성공', data: videos });
  } catch (error) {
    res.status(500).json({ message: '❌ keywords_popular_videos 데이터 조회 실패', error });
  }
});

// 특정 키워드에 대한 인기 영상 조회 API
router.get('/mongo-popular-videos/:keyword', async (req, res) => {
  try {
    const keyword = req.params.keyword;
    const videos = await PopularVideo.findOne({ keyword }); // 특정 키워드 데이터 찾기

    if (!videos) {
      return res.status(404).json({ message: `❌ '${keyword}'에 대한 인기 영상이 없습니다.` });
    }

    res.json({ message: '✅ 인기 영상 데이터 조회 성공', data: videos });
  } catch (error) {
    res.status(500).json({ message: '❌ 인기 영상 데이터 조회 실패', error });
  }
});


module.exports = router;
