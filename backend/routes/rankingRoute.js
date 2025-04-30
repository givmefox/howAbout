// backend/routes/rankingRoute.js
const express = require("express");
const router = express.Router();
const { spawn } = require("child_process");
const path = require("path");

router.get("/ranking/:period", (req, res) => {
  const period = req.params.period;

  let script;
  if (period === "today") script = "ranking_today.py";
  else if (period === "week") script = "ranking_week.py";
  else if (period === "month") script = "ranking_month.py";
  else return res.status(400).json({ error: "❌ 잘못된 기간" });

  const pythonPath = "../youtube/.venv/Scripts/python.exe";
  const scriptPath = path.join(__dirname, "../", script);

  const py = spawn(pythonPath, [scriptPath]);
  let result = "";

  py.stdout.setEncoding("utf-8");
  py.stdout.on("data", (data) => {
    result += data.toString();
    console.log("📥 PYTHON STDOUT:", data.toString());
  });

  py.stderr.on("data", (data) => {
    console.error("🐍 PYTHON STDERR:", data.toString());
  });

  py.on("close", (code) => {
    console.log("PYTHON 종료 코드:", code);
    if (code === 0) {
      try {
        const parsed = JSON.parse(result);
        res.json(parsed);
      } catch (e) {
        console.error("❌ JSON 파싱 실패:", e);
        res.status(500).json({ error: "❌ JSON 파싱 실패", raw: result });
      }
    } else {
      console.error("❌ Python 실행 실패, 종료 코드:", code);
      res.status(500).json({ error: "❌ Python 실행 실패", raw: result });
    }
  });
});

module.exports = router; // ✅ 꼭 router 객체를 export 해야 함
