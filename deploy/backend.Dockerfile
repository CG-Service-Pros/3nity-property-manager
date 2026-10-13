FROM node:22-bookworm-slim AS build
ENV PUPPETEER_SKIP_DOWNLOAD=true PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true HUSKY=0
RUN apt-get update && apt-get install -y --no-install-recommends python3 make g++ ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/app
COPY package.json yarn.lock .yarnrc.yml ./
COPY .yarn/plugins .yarn/plugins
COPY .yarn/releases .yarn/releases
COPY types types
COPY services services
RUN node .yarn/releases/yarn-3.3.0.cjs workspaces focus @microrealestate/api @microrealestate/authenticator @microrealestate/gateway @microrealestate/tenantapi @microrealestate/emailer @microrealestate/pdfgenerator
RUN node .yarn/releases/yarn-3.3.0.cjs workspace @microrealestate/types build && node .yarn/releases/yarn-3.3.0.cjs workspace @microrealestate/common build && node .yarn/releases/yarn-3.3.0.cjs workspace @microrealestate/gateway build && node .yarn/releases/yarn-3.3.0.cjs workspace @microrealestate/tenantapi build

FROM build AS runtime
ENV NODE_ENV=production CHROMIUM_BIN=/usr/bin/chromium
RUN apt-get update && apt-get install -y --no-install-recommends chromium fonts-liberation fonts-noto-color-emoji && rm -rf /var/lib/apt/lists/*
RUN mkdir -p services/pdfgenerator/tmp services/pdfgenerator/pdf_documents services/pdfgenerator/uploads services/emailer/tmp backup && chown -R node:node /usr/app
COPY LICENSE /usr/app/LICENSE
USER node
CMD ["node", "services/api/src/index.js"]
