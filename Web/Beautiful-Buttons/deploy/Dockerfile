FROM node:21-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libgtk-3-0 \
    libasound2 libxshmfence1 libx11-xcb1

WORKDIR /app

COPY app/.puppeteerrc.cjs app/package.json app/package-lock.json ./
RUN npm ci && npm cache clean --force


COPY app .

ENV PORT=8080

CMD ["node", "index.js"]
