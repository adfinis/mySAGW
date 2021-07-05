FROM node:lts-slim

WORKDIR /usr/share/app
COPY . /usr/share/app

ARG OIDC_HOST

RUN apt-get update && apt-get -y install git

RUN yarn install && yarn build

FROM nginx:alpine as final
COPY --from=0 /usr/share/app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
