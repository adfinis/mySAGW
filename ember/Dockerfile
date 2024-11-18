FROM danlynn/ember-cli:5.8.1-node_20.12 as build

ARG OIDC_HOST

COPY package.json yarn.lock /myapp/

RUN yarn install

COPY . /myapp/

RUN yarn deploy production

FROM nginx:alpine

COPY --from=build /myapp/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
