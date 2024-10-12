const express = require('express');
const router = express.Router();
const Admin = require('../models/Admin');

const FLAG = process.env.FLAG || 'flag{fake_flag_for_testing}';

router.get('/login', (req, res) => {
    res.render('adminLogin');
});

router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const admin = await Admin.findOne({ username, password });

    if (admin) {
        req.session.admin = admin;
        res.redirect('/admin/index');
    } else {
        res.redirect('/admin/login');
    }
});

router.get('/index', (req, res) => {
    // if (!req.session.admin) {
    //     return res.redirect('/admin/login');
    // }
    res.render('adminIndex', { flag: FLAG });
});

module.exports = router;
