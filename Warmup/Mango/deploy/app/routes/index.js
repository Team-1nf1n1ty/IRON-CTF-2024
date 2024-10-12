// routes/index.js

const express = require('express');
const router = express.Router();
const Fruit = require('../models/Fruit');

router.get('/', async (req, res) => {
    const fruits = await Fruit.find();
    res.render('fruit', { fruits });
});

module.exports = router;
