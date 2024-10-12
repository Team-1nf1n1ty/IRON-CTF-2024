// This code is just for reference
const page = await browser.newPage();
await page.goto(urlToVisit, {
    waitUntil: 'networkidle2',
});
await page.goto(`${CONFIG.APPURL}/login`, { waitUntil: 'networkidle2' });
await page.focus('input[name=username]');
await page.keyboard.type(CONFIG.ADMIN_USERNAME);
await page.focus('input[name=password]');
await page.keyboard.type(CONFIG.ADMIN_PASS);
await page.click('input[type="submit"]');
await sleep(1000)
await page.close()