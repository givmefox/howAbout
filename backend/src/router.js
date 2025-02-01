const express = require('express');
const router = express.Router();

const authenticateToken = require('./middleware/authMiddleware');

//controller


//router
// router.get('/', webController.home);

router.post('/auth/register', apiUserController.register);
module.exports = router;

