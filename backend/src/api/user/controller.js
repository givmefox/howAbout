const repository = require("./repository");
const bcrypt = require("bcryptjs"); // bcrypt 사용
const jwt = require("jsonwebtoken");

require("dotenv").config(); // 환경 변수 로드

// 🔹 회원가입
exports.register = async (req, res) => {
  const { userid, username, password } = req.body;

  try {
    // 1️⃣ 아이디 중복 확인
    let { count } = await repository.checkId(userid);
    if (count > 0) {
      return res.status(400).json({ result: "fail", message: "이미 존재하는 아이디입니다." });
    }

    // 2️⃣ 비밀번호 해싱 (bcrypt 사용)
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // 3️⃣ 회원 정보 저장
    const { affectedRows, insertId } = await repository.register(userid, username, hashedPassword);
    
    if (affectedRows > 0) {
      // 4️⃣ JWT 토큰 생성
      const token = jwt.sign(
        { userid: insertId, username: username },
        process.env.JWT_SECRET,
        { expiresIn: "1h" }
      );

      return res.status(201).json({ result: "ok", access_token: token, message: "회원가입 성공!" });
    } else {
      return res.status(500).json({ result: "fail", message: "회원가입 실패!" });
    }
  } catch (error) {
    console.error("❌ 회원가입 오류:", error);
    return res.status(500).json({ result: "fail", message: error.message });
  }
};

// 🔹 로그인
exports.login = async (req, res) => {
  const { userid, password } = req.body;

  try {
    // 1️⃣ 사용자 정보 조회
    const user = await repository.getUserById(userid);
    
    if (!user) {
      return res.status(401).json({ result: "fail", message: "존재하지 않는 아이디입니다." });
    }

    // 2️⃣ 비밀번호 검증 (bcrypt 비교)
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ result: "fail", message: "비밀번호가 일치하지 않습니다." });
    }

    // 3️⃣ JWT 토큰 생성
    const token = jwt.sign(
      { userid: user.userid, username: user.username },
      process.env.JWT_SECRET,
      { expiresIn: "1h" }
    );

    return res.status(200).json({
      result: "ok",
      access_token: token,
      userid: user.userid,
      username: user.username,
      message: "로그인 성공!"
    });

  } catch (error) {
    console.error("❌ 로그인 오류:", error);
    return res.status(500).json({ result: "fail", message: error.message });
  }
};
