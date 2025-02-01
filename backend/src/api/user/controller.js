const repository = require('./repository');
const crypto = require('crypto');
const jwt = require('./jwt');

// 회원가입
exports.register = async (req, res) => {
    const { id, username, password } = req.body;

    let {count} = await repository.checkId(id);

    //아이디 중복 확인
    if(count > 0) {
        return res.json({ result: 'fail', message: '이미 존재하는 아이디 입니다.' });
    }

    //비밀번호 암호화
    const result = await crypto.pbkdf2Sync(password, process.env.SALT_KEY, 50, 100, 'sha512');

    //회원가입 
    const {affectedRows, insertId} = await repository.register(id, username, result.toString('base64'));

    if(affectedRows > 0) {
        const  data = await jwt({id: insertId, username: username});
        res.json({ result: 'ok', access_token: data });
    } else {
        res.json({ result: 'fail', message: '회원가입 실패' });
    }
}


// 로그인
exports.login = async (req, res) => {
    const { id, password } = req.body;

    const result = await crypto.pbkdf2Sync(password, process.env.SALT_KEY, 50, 100, 'sha512');
    const item = await repository.login(id, result.toString('base64'));

    if (item === null) {
        res.json({ result: 'fail', message: '아이디 또는 비밀번호가 일치하지 않습니다.' });
    } else {
        const data = await jwt({id: item.id, username: item.username});
        res.json({ result: 'ok', access_token: data });
    }
}