const res = require('express/lib/response');
const {pool} = require('../../database');

exports.register = async (id, username, password) => {
    const query = `INSERT INTO user (id, username, password) VALUES (?, ?, ?)`;
    return await pool.query(query, [id, username, password]);
}

exports.login = async (id, password) => {
    const query = `SELECT * FROM user WHERE id = ? AND password = ?`;
    let result = await pool.query(query, [id, password]);
    return (result.length === 0) ? null : result[0];
}