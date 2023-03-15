FROM danlynn/ember-cli:4.12.1 as build

ARG OIDC_HOST

COPY package.json pnpm-lock.yaml /myapp/

RUN npm install -g pnpm

RUN pnpm install

COPY . /myapp/

RUN pnpm run deploy production

FROM nginx:alpine

COPY --from=build /myapp/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
