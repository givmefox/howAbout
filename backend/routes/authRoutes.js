const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('../src/database');
const dotenv = require('dotenv');

dotenv.config();
const router = express.Router();

//회원가입 API
router.post('/register', async (req, res) => {
  const { id, username, password } = req.body;

  if (!id || !username || !password) {
    return res.status(400).json({ message: "모든 필드를 입력하세요." });
  }

  const hashedPassword = await bcrypt.hash(password, 10);
  const newUser = await db.query(
    'INSERT INTO users (id, username, password) VALUES ($1, $2, $3) RETURNING *',
    [id, username, hashedPassword]
  );

  const user = newUser.rows[0];
  const token = jwt.sign({ id: user.id, username: user.username }, process.env.JWT_SECRET, {
    expiresIn: '1h'
  });
  res.status(201).json({ token });
});

module.exports = router;