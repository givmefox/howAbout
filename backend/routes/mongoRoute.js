const express = require("express");
const router = express.Router();
const mongoose = require("../src/database/mongodb"); // MongoDB 연결 파일

// MongoDB users 컬렉션 모델 정의
const UserSchema = new mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId, // MongoDB ObjectId
  name: String,
  age: Number,
});
const User = mongoose.model("User", UserSchema, "users"); // 컬렉션명: users

// MongoDB category_keywords 컬렉션 모델 정의
const CategoryKeywordSchema = new mongoose.Schema({
  category: String,
  ranked_keywords: [
    {
      순위: Number,
      키워드: String,
    },
  ],
});
const CategoryKeyword = mongoose.model(
  "CategoryKeyword",
  CategoryKeywordSchema,
  "category_keywords"
);

// MongoDB keyword_videos 컬렉션 모델 정의
const KeywordVideoSchema = new mongoose.Schema({
  category: String,
  keywords: [
    {
      keyword: String,
      videos: [
        {
          video_id: String,
          score: Number,
          title: String,
        },
      ],
    },
  ],
});
const KeywordVideo = mongoose.model(
  "KeywordVideo",
  KeywordVideoSchema,
  "keyword_videos"
);

// MongoDB related_keywords 컬렉션 모델 정의
const RelatedKeywordSchema = new mongoose.Schema({
  category: String,
  keywords: [
    {
      keyword: String,
      related: [String],
    },
  ],
});
const RelatedKeyword = mongoose.model(
  "RelatedKeyword",
  RelatedKeywordSchema,
  "related_keywords"
);

// ✅ API1 : MongoDB에서 users 데이터 가져오기
router.get("/mongo-users", async (req, res) => {
  try {
    const users = await User.find(); // 모든 사용자 조회
    res.json({ message: "✅ MongoDB 데이터 조회 성공", data: users });
  } catch (error) {
    res.status(500).json({ message: "❌ MongoDB 데이터 조회 실패", error });
  }
});

// ✅ API 2: category_keywords 데이터 조회
router.get("/mongo-category-keywords", async (req, res) => {
  try {
    const categories = await CategoryKeyword.find(); // 모든 데이터 조회
    res.json({
      message: "✅ category_keywords 데이터 조회 성공",
      data: categories,
    });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ category_keywords 데이터 조회 실패", error });
  }
});

// ✅ API 3: keyword_videos 데이터 조회
router.get("/mongo-keyword-videos", async (req, res) => {
  try {
    const videos = await KeywordVideo.find(); // 모든 데이터 조회
    res.json({ message: "✅ keyword_videos 데이터 조회 성공", data: videos });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ keyword_videos 데이터 조회 실패", error });
  }
});

// ✅ 특정 카테고리의 keyword_videos 조회
router.get("/mongo-keyword-videos/:category", async (req, res) => {
  try {
    const category = req.params.category;
    const videos = await KeywordVideo.findOne({ category });

    if (!videos) {
      return res
        .status(404)
        .json({ message: `❌ '${category}' 카테고리의 데이터가 없습니다.` });
    }

    res.json({ message: "✅ keyword_videos 데이터 조회 성공", data: videos });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ keyword_videos 데이터 조회 실패", error });
  }
});

// ✅ API 4: related_keywords 데이터 조회
router.get("/mongo-related-keywords", async (req, res) => {
  try {
    const keywords = await RelatedKeyword.find(); // 모든 데이터 조회
    res.json({
      message: "✅ related_keywords 데이터 조회 성공",
      data: keywords,
    });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ related_keywords 데이터 조회 실패", error });
  }
});

// ✅ 특정 키워드의 related_keywords 조회
router.get("/mongo-related-keywords/:keyword", async (req, res) => {
  try {
    const keyword = req.params.keyword;
    const result = await RelatedKeyword.findOne(
      { "keywords.keyword": keyword },
      { "keywords.$": 1 }
    );

    if (!result) {
      return res
        .status(404)
        .json({ message: `❌ '${keyword}'에 대한 연관 키워드가 없습니다.` });
    }

    res.json({ message: "✅ related_keywords 데이터 조회 성공", data: result });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ related_keywords 데이터 조회 실패", error });
  }
});

module.exports = router;
