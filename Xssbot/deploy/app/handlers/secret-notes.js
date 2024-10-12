

const CONFIG = {
    DISPLAY: process.env.CHALL_SECRET_NOTES_DISPLAY,
    NAME: process.env.CHALL_SECRET_NOTES_NAME,
    APPURL: process.env.CHALL_SECRET_NOTES,
    ADMIN_USERNAME: process.env.CHALL_SECRET_NOTES_USERNAME,
    ADMIN_PASS: process.env.CHALL_SECRET_NOTES_PASS,
    APPURLREGEX: process.env.APPURLREGEX || /^.*$/,
    APPLIMITTIME: 60,
    APPLIMIT: 2,
    TIMEOUT: 5000,
}

console.table(CONFIG);

function sleep(s) {
    return new Promise((resolve) => setTimeout(resolve, s))
}

module.exports = {
    pageDisplay: CONFIG.DISPLAY,
    name: CONFIG.NAME,
    urlRegex: CONFIG.APPURLREGEX,
    rateLimit: {
        windowS: CONFIG.APPLIMITTIME,
        max: CONFIG.APPLIMIT
    },
    async execute(browser, urlToVisit) {
        try {
            const page = await browser.newPage();
            const start = performance.now()
            await page.goto(urlToVisit, {
                waitUntil: 'networkidle2',
                timeout: CONFIG.TIMEOUT,
            });
            await page.goto(`${CONFIG.APPURL}/login`, { waitUntil: 'networkidle2' });
            await page.focus('input[name=username]');
            await page.keyboard.type(CONFIG.ADMIN_USERNAME);
            await page.focus('input[name=password]');
            await page.keyboard.type(CONFIG.ADMIN_PASS);
            await page.click('input[type="submit"]');
            await sleep(2000)
            await page.close()
            const end = performance.now()
            console.log(`${CONFIG.NAME}: ${urlToVisit} page closed in ${end - start}ms`)
            return true;
        } catch (e) {
            console.error(e);
            return false;
        }
    }
}