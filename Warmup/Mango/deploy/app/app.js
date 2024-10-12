const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const mongoose = require('mongoose');
const path = require('node:path');
const fs = require('node:fs');

const app = express();
const PORT = 3000;

// Connect to MongoDB
mongoose.connect('mongodb://mongo-mango:27017/mango', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log("Connected to MongoDB");
}).catch(err => {
    console.error("MongoDB connection error:", err);
});

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
    secret: 'secretKeydafb25b2bccab6c3ae13aad90fa862439d9ab98c',
    resave: false,
    saveUninitialized: true
}));

// Set view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(`${__dirname}/public`));

// Load fruit data from JSON
const fruitData = JSON.parse(fs.readFileSync(path.join(__dirname, 'fruits.json')));

// Routes
app.get('/', (req, res) => {
    res.render('index', { fruits: fruitData });
});

// Admin routes
app.use('/admin', require('./routes/admin'));

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
