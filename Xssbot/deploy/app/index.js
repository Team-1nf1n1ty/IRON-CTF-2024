require("dotenv").config({ path: ["chall.env", ".env", "infra.env"] });
const os = require('node:os');
const express = require("express");
const axios = require("axios");
const fs = require("node:fs");
const path = require("node:path");
const puppeteer = require("puppeteer");

const app = express();

const port = Number(process.env.PORT) || 8085;

const submitPage = fs.readFileSync(path.join(__dirname, "submit.html"), "utf8");

function replace(str, old, rep) {
    return str.replaceAll(old, rep.replaceAll("$", "$$$$"));
}

function sleep(ms) {
    return new Promise((res) => setTimeout(res, ms));
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
        '--disable-xss-auditor'
    ],
});

app.use(express.urlencoded({ extended: false }));

for (const f of fs.readdirSync(path.join(__dirname, "handlers"))) {
    if (f.endsWith(".js")) {
        const handler = require(`./${path.join("handlers", f)}`);
        let page = replace(submitPage, "$NAME", handler.pageDisplay);
        page = replace(page, "$PATH", handler.name);
        page = replace(
            page,
            "$RECAPTCHA_SITE",
            process.env.RECAPTCHA_SITE || ""
        );
        page = replace(
            page,
            "$RECAPTCHA_SECRET",
            process.env.RECAPTCHA_SECRET || ""
        );
        app.get(`/${handler.name}`, (req, res) => {
            res.type("text/html").send(page);
        });
        app.post(`/${handler.name}`, async (req, res) => {
            const url = req.body.url;
            if (!(handler.urlRegex || /^https?:\/\//).test(url)) {
                return res.status(400).send({ error: "I won't go to random links." });
            }
            if (process.env.RECAPTCHA_SITE && process.env.RECAPTCHA_SECRET) {
                try {
                    const body = new URLSearchParams({
                        secret: process.env.RECAPTCHA_SECRET,
                        response: req.body["g-recaptcha-response"],
                    });
                    const resp = await axios.post(
                        "https://www.google.com/recaptcha/api/siteverify",
                        body
                    );
                    if (!resp.data.success) {
                        return res.send({ error: "Invalid captcha." });
                    }
                } catch (err) {
                    console.error("Captcha verification failure", err);
                    return res.status(400).send({ error: "Captcha verification failure." });
                }
            }
            let context;
            let bot_status = undefined;
            try {
                context = await (await browser).createBrowserContext();
                const prom = handler.timeout
                    ? Promise.race([
                        handler.execute(context, url),
                        sleep(handler.timeout),
                    ])
                    : handler.execute(context, url);
                bot_status = await prom;
            } catch (err) {
                console.error("Handler error", err);
                if (context) {
                    try {
                        await context.close();
                    } catch (e) {
                        console.log(e);
                    }
                }
                return res.status(400).send({ error: "Error visiting page." });
            }
            try {
                await context.close();
            } catch (e) {
                console.log(e)
                return res.status(400).send({ error: "Something is wrong." });

            }
            if (bot_status) {
                return res.send({ success: "Admin successfully visited the URL." });
            }
            return res.status(400).send({ error: "Something went wrong" });
        });
        console.log(`Registered handler for ${handler.name}.`);
    }
}

app.get("/", (req, res) => {
    const hostname = os.hostname();
    res.send(`admin bot is up <!-- ${hostname} -->`);
});

app.listen(port, () => {
    console.log(`App listening on port ${port}.`);
});
