const mysql = require('mysql2');
const dotenv = require('dotenv');

dotenv.config();


//mysql 연결
const db = mysql.createConnection({
  host: process.env.DB_HOST,  // DB서버 IP주소
  user: process.env.DB_USER,  // DB접속 아이디
  password: process.env.DB_PASSWORD,  // DB암호
  database: process.env.DB_DATABASE,  //사용할 DB명
  port: process.env.DB_PORT // DB 포트
});

db.connect((err) => {
  if (err) {
    console.error('mysql connection error');
    console.error(err);
    throw err;
  } else {
    console.log('mysql connection success');
  }
});

module.exports = db;