const repository = require("./repository");
const crypto = require("crypto");
const jwt = require("jsonwebtoken");

require("dotenv").config(); // 환경 변수를 로드합니다.

// 회원가입
exports.register = async (req, res) => {
  const { userid, username, password } = req.body;

  try {
    let { count } = await repository.checkId(userid);

    // 아이디 중복 확인
    if (count > 0) {
      return res.json({
        result: "fail",
        message: "이미 존재하는 아이디 입니다.",
      });
    }

    // 비밀번호 암호화
    const salt = process.env.SALT_KEY;
    if (!salt) {
      throw new Error("SALT_KEY 환경 변수가 설정되지 않았습니다.");
    }

    const hashedPassword = await new Promise((resolve, reject) => {
      crypto.pbkdf2(password, salt, 50, 100, "sha512", (err, derivedKey) => {
        if (err) reject(err);
        resolve(derivedKey.toString("base64"));
      });
    });

    // 회원가입
    const { affectedRows, insertId } = await repository.register(
      userid,
      username,
      hashedPassword
    );

    if (affectedRows > 0) {
      const token = jwt.sign(
        { userid: insertId, username: username },
        process.env.JWT_SECRET,
        {
          expiresIn: "1h",
        }
      );
      res.status(201).json({ result: "ok", access_token: token, data: "success" });
    } else {
      res.status(500).json({ result: "fail", message: "회원가입 실패" });
    }
  } catch (error) {
    res.status(500).json({ result: "fail", message: error.message });
  }
};

// 로그인
exports.login = async (req, res) => {
  const { userid, password } = req.body;

  try {
    const salt = process.env.SALT_KEY;
    const hashedPassword = await new Promise((resolve, reject) => {
      crypto.pbkdf2(password, salt, 50, 100, "sha512", (err, derivedKey) => {
        if (err) reject(err);
        resolve(derivedKey.toString("base64"));
      });
    });

    const user = await repository.login(userid, hashedPassword);

    if (!user) {
      res.status(401).json({
        result: "fail",
        message: "아이디 또는 비밀번호가 일치하지 않습니다.",
      });
    } else {
      const token = jwt.sign(
        { userid: user.id, username: user.username },
        process.env.JWT_SECRET,
        {
          expiresIn: "1h",
        }
      );
      res.status(200).json({ result: "ok", access_token: token });
    }
  } catch (error) {
    res.status(500).json({ result: "fail", message: error.message });
  }
};
