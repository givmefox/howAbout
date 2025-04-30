require("dotenv").config();
const express = require("express");
const mysql = require("./src/database/index"); // MySQL 연결
const mongoose = require("./src/database/mongodb"); // MongoDB 연결
const cors = require("cors");
const app = express();
const { spawn } = require("child_process");
const path = require("path");
const port = 3000; // 백엔드 실행 포트
const router = require("./src/router");
const bodyParser = require("body-parser");
const mongoRoutes = require("./routes/mongoRoute"); // MongoDB 라우트
const authRoutes = require("./routes/authRoutes.js");
const fs = require("fs");
const rankingRoutes = require("./routes/rankingRoute");

app.use("/auth", authRoutes); // 이게 있어야 /auth/login 가능함

app.use(
  cors({
    origin: "*", // 모든 출처 허용 (보안이 필요하면 도메인 지정)
    methods: ["GET", "POST", "PUT", "DELETE"],
    credentials: true,
  })
);

app.use("/api", rankingRoutes);
// JSON 형식의 데이터 처리
app.use(bodyParser.json());
// URL 인코딩 된 데이터 처리
app.use(bodyParser.urlencoded({ extended: true }));

// 라우터를 애플리케이션에 등록
app.use("/", router);
app.use("/api", mongoRoutes);

// 테스트 API: MySQL 연결 확인
app.get("/mysql-test", async (req, res) => {
  try {
    const [rows] = await mysql.query("SELECT 1 + 1 AS result");
    res.json({ message: "✅ MySQL 연결 성공", data: rows });
  } catch (err) {
    res.status(500).json({ message: "❌ MySQL 연결 실패", error: err });
  }
});

// ✅ MongoDB 랭킹 데이터 가져오기 API
app.get("/api/mongo-rank", async (req, res) => {
  try {
    const rankings = await mongoose.connection.db
      .collection("rankings")
      .find()
      .toArray();
    res.json({ message: "✅ 랭킹 데이터 불러오기 성공", data: rankings });
  } catch (error) {
    res.status(500).json({ message: "❌ 랭킹 데이터 불러오기 실패", error });
  }
});

// ✅ MongoDB 연결 테스트 API
app.get("/mongo-test", async (req, res) => {
  try {
    const collections = await mongoose.connection.db
      .listCollections()
      .toArray();
    res.json({ message: "✅ MongoDB 연결 성공", collections });
  } catch (err) {
    res.status(500).json({ message: "❌ MongoDB 연결 실패", error: err });
  }
});

app.get("/api/keywords-popular-videos", async (req, res) => {
  try {
    const videos = await mongoose.connection.db
      .collection("keywords_popular_videos")
      .find()
      .toArray();
    res.json({
      message: "✅ 키워드 인기 영상 데이터 불러오기 성공",
      data: videos,
    });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ 키워드 인기 영상 데이터 불러오기 실패", error });
  }
});

app.get("/api/related-keywords", async (req, res) => {
  try {
    const relatedKeywords = await mongoose.connection.db
      .collection("related_keywords")
      .find()
      .toArray();
    res.json({
      message: "✅ 관련 키워드 데이터 불러오기 성공",
      data: relatedKeywords,
    });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ 관련 키워드 데이터 불러오기 실패", error });
  }
});

app.get("/run-audio", (req, res) => {
  const youtubeUrl = req.query.url;

  if (!youtubeUrl) {
    return res
      .status(400)
      .json({ error: "❌ 유튜브 URL이 필요합니다. (url=...)" });
  }

  const scriptPath = path.join(__dirname, "audio.py");
  const python = spawn("../youtube/.venv/Scripts/python.exe", [
    scriptPath,
    youtubeUrl,
  ]);

  let result = "";
  let error = "";

  python.stdout.on("data", (data) => {
    result += data.toString();
    console.log("✅ PYTHON STDOUT (raw):", result);
  });

  python.stderr.on("data", (data) => {
    error += data.toString();
    console.error("🐍 PYTHON STDERR:", data.toString());
  });

  python.on("close", (code) => {
    if (code === 0) {
      try {
        res.json(JSON.parse(result));
      } catch (e) {
        res.status(500).json({
          error: "❌ JSON 파싱 실패",
          raw: result,
        });
      }
    } else {
      res.status(500).json({
        error: "❌ Python 실행 중 오류 발생",
        detail: error,
      });
    }
  });
});

app.get("/api/keyword-detail/:keyword", (req, res) => {
  const keyword = decodeURIComponent(req.params.keyword);
  const jsonPath = path.join(__dirname, "../youtube/test/graded_keywords.json");

  fs.readFile(jsonPath, "utf-8", (err, data) => {
    if (err) {
      console.error("❌ JSON 파일 읽기 실패:", err);
      return res.status(500).json({ error: "서버 내부 오류" });
    }

    try {
      const parsed = JSON.parse(data);

      let found = null;
      for (const category in parsed) {
        if (parsed[category][keyword]) {
          found = parsed[category][keyword];
          break;
        }
      }

      if (found) {
        res.json(found);
      } else {
        res
          .status(404)
          .json({ error: "해당 키워드 분석 결과를 찾을 수 없습니다." });
      }
    } catch (e) {
      console.error("❌ JSON 파싱 실패:", e);
      res.status(500).json({ error: "JSON 파싱 오류" });
    }
  });
});

// 서버 실행
app.listen(port, "0.0.0.0", () => {
  console.log(`✅ 서버 실행 중: http://0.0.0.0:${port}`);
});
