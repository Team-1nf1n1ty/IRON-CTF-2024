const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const { v4: uuidv4 } = require('uuid');
const crypto = require('node:crypto');
const puppeteer = require("puppeteer");
const fs = require('node:fs');
const rateLimit = require('express-rate-limit');

require("dotenv").config({ path: [".env"] });

const FLAG = process.env.FLAG || "ironCTF{testing123}"
const PORT = process.env.PORT || 3000;
const MONGODB_URL = process.env.MONGODB_URL || "mongodb://localhost:27017/";
const TIMEOUT = 4500
const TokenLife = process.env.TOKEN_LIFE || 8000

const pdflimiter = rateLimit({
    windowMs: TokenLife*60,
    max: 100,
    headers: true,
    keyGenerator: (req) => req.body.auth_key,
    handler: (req, res, next) => {
        const uid = req.body.auth_key;
        if (uid) {
            const [token, time] = PlayerAdminToken.getTokenByUserID(uid);
            PlayerAdminToken.deleteToken(token)
        }
        res.status(429).json({
            message: "Your key got deleted for voilation of ratelimit goto /pow to get a new key."
        });
    }
});

const ipLimiter = rateLimit({
    windowMs: TokenLife*60,
    max: 100,
    headers: true, 
    keyGenerator: (req) => req.headers['x-real-ip'],
    handler: (req, res) => {
        const uid = req.body.auth_key;
        if (uid) {
            const [token, time] = PlayerAdminToken.getTokenByUserID(uid);
            PlayerAdminToken.deleteToken(token)
        }
        res.status(429).json({
            message: "Your key got deleted for voilation of ratelimit goto /pow to get a new key."
        });
    }
});

const flaglimiter = rateLimit({
    windowMs: TokenLife*60,
    max: 1,
    headers: true,
    keyGenerator: (req) => req.body.auth_key,
    handler: (req, res, next) => {
        const uid = req.body.auth_key;
        if (uid) {
            const [token, time] = PlayerAdminToken.getTokenByUserID(uid);
            PlayerAdminToken.deleteToken(token)
        }
        res.status(429).json({
            message: "Don't brute the token, Your key got deleted for voilation of ratelimit goto /pow to get a new key."
        });
    }
});

const checkAuthKey = (req, res, next) => {
    if (!req.body.auth_key) {
        return res.status(401).json({ message: 'auth_key is required' });
    }
    const [token, _] = PlayerAdminToken.getTokenByUserID(req.body.auth_key)
    if (token) {
        next();
    } else {
        return res.status(401).json({ message: 'auth_key is expired' });
    }

};


class AdminTokenManager {
    constructor(expirationTime) {
        this.expirationTime = expirationTime;
        this.tokens = new Map();
        setInterval(() => {
            this.cleanupExpiredTokens();
        }, 1000);
    }

    generateRandomHex() {
        return crypto.randomBytes(3).toString('hex');
    }

    createToken(userid) {
        const token = this.generateRandomHex();
        const createdAt = Date.now();
        this.tokens.set(token, { createdAt, userid });
        return token;
    }

    deleteToken(token) {
        if (this.tokens.has(token)) {
            this.tokens.delete(token);
            return true
        }
        return false
    }

    cleanupExpiredTokens() {
        const currentTime = Date.now();
        for (const [token, metadata] of this.tokens.entries()) {
            if (currentTime - metadata.createdAt >= this.expirationTime) {
                this.tokens.delete(token);
            }
        }
    }

    getAllTokens() {
        return Array.from(this.tokens.keys());
    }
    getAllEntries() {

        return Array.from(this.tokens.entries());
    }
    getTokenByUserID(userid) {
        for (const [token, metadata] of this.tokens.entries()) {
            if (metadata.userid === userid) {
                return [token, metadata.createdAt];
            }
        }
        return [false, false];
    }
}


const browser = puppeteer.launch({
    headless: true,
    args: [
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--no-gpu',
        '--disable-default-apps',
        '--disable-translate',
        '--disable-device-discovery-notifications',
        '--disable-software-rasterizer',
        '--disable-xss-auditor',
        "--start-maximized",
        '--metrics-recording-only',
        '--disable-sync',
        '--no-first-run',
        '--disable-extensions',
        '--disable-background-networking',
    ],
});

const PlayerAdminToken = new AdminTokenManager(TokenLife * 60)
const app = express();

mongoose.connect(`${MONGODB_URL}buttonGenerator?authSource=admin`);

function isValid(uuid) {
    const uuidV4Regex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    return uuidV4Regex.test(uuid);
}

const buttonSchema = new mongoose.Schema({
    id: { type: String, default: uuidv4 },
    bgcolor: String,
    text: String,
    size: String,
    borderRadius: String,
});

const Button = mongoose.model('Button', buttonSchema);

app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));
app.use((req, res, next) => {
    // safe :)
    res.setHeader("Content-Security-Policy", "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'none'; font-src 'none'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self';script-src-elem 'self' https://www.gstatic.com/recaptcha/releases/EGbODne6buzpTnWrrBprcfAY/recaptcha__en.js; frame-src https://www.google.com/");
    next();
});


app.get('/', (req, res) => {
    res.render('index');
});

app.post('/generate', async (req, res) => {
    const { bgcolor, text, size, borderRadius } = req.body;
    if (text > 20) {
        res.status(400).send("BTN text too big.....")
    }
    const newButton = new Button({ bgcolor, text, size, borderRadius });
    await newButton.save();
    res.redirect(`/show/${newButton.id}`);
});


app.get('/show/:id', async (req, res) => {
    res.render('index');
});


app.get('/button/:id', async (req, res) => {
    const button = await Button.findOne({ id: req.params.id }).select('-_id -__v -id');
    if (!button) {
        return res.status(404).json({ "Error": 'Button not found' });
    }
    return res.json(button)
});


app.post("/report", checkAuthKey, ipLimiter, pdflimiter, async (req, res) => {
    const { post_id, auth_key } = req.body;
    console.table(req.headers);
    if (isValid(post_id)) {
        const exists = Button.findOne({ id: post_id });
        if (!exists) {
            return res.status(404).json({ "Error": 'Button not found' });
        }
        const url = `http://localhost:${PORT}/show/${post_id}`
        const [playerToken, _] = PlayerAdminToken.getTokenByUserID(auth_key)
        console.table(PlayerAdminToken.getAllEntries());
        const context = await (await browser).createBrowserContext();
        try {
            const page = await context.newPage();
            await page.setViewport({ width: 1920, height: 1080 });
            await page.setCookie({
                name: "token",
                httpOnly: false,
                value: playerToken,
                url: `http://localhost:${PORT}`
            })
            const start = performance.now()
            await page.goto(url, {
                waitUntil: 'networkidle0',
                timeout: TIMEOUT
            });
            await page.pdf({
                path: `pdfs/${post_id}.pdf`,
                format: 'A4',
                printBackground: true,
                margin: {
                    top: '20px',
                    bottom: '20px',
                    left: '20px',
                    right: '20px'
                }
            });
            await page.close()
            await context.close()
            const end = performance.now()
            const ip = req.headers["x-real-ip"];
            fs.unlink(`pdfs/${post_id}.pdf`, (err) => {
                if (err) {
                    console.error(`Error removing file: ${err.message}`);
                }
            });
            return res.json({ "feedback": 'Not that great!!' });
        } catch (error) {
            await context.close()
            if (error.message.includes('Navigation timeout')) {
                console.error(`Navigation timed out by ${auth_key}: `, error.message);
            } else {
                console.error("An unexpected error occurred:", error);
            }
            return res.status(500).json({ "feedback": "Something went wrong!!" });
        }
    }
    return res.json({ "Error": "Try Harder!!!!" })
})


app.post("/admin", checkAuthKey, flaglimiter, async (req, res) => {
    const { UserAdminToken, auth_key } = req.body;
    const [token, _] = PlayerAdminToken.getTokenByUserID(auth_key)
    if (token === UserAdminToken) {
        PlayerAdminToken.deleteToken(UserAdminToken);
        return res.json({ "flag": FLAG })
    }
    return res.json({ "Error": "Try Harder!!!!" })
})
// Not related to challenge !!
app.post("/pow", async (req, res) => {
    const { 'g-recaptcha-response': recaptchaResponse } = req.body;
    try {
        const verificationUrl = `https://www.google.com/recaptcha/api/siteverify?secret=${process.env.RECAPTCHA_SECRET}&response=${recaptchaResponse}`;

        // Use fetch instead of axios
        const response = await fetch(verificationUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        if (!response.ok) {
            throw new Error(`Error during reCAPTCHA verification: ${response.statusText}`);
        }

        const responseData = await response.json();
        const { success, 'error-codes': errorCodes } = responseData;

        if (!success) {
            return res.status(400).send(`reCAPTCHA verification failed. Error codes: ${errorCodes}`);
        }

        const uniqueId = uuidv4();
        PlayerAdminToken.createToken(uniqueId);
        res.send(`Registration successful! your apikey ${uniqueId}. You have to send this to /admin, /report, and it will be active for ${TokenLife / 1000} mins.`);
    } catch (error) {
        console.error('Error during reCAPTCHA verification:', error);
        res.status(500).send('Internal Server Error');
    }
})
app.get("/pow", async (req, res) => {
    if (req.query.ttl) {
        const [num, ttl] = PlayerAdminToken.getTokenByUserID(req.query.ttl)
        if (num) {
            const ttlsecs = (PlayerAdminToken.expirationTime - (Date.now() - ttl)) / (1000)
            return res.json({ "ttl": `session will expire in ${ttlsecs} seconds.` })
        }
        return res.json({ "error": "Expired/ Not-registered" })

    }
    return res.render('pow', { key_site: process.env.RECAPTCHA_SITE });
})




app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
