FROM danlynn/ember-cli:latest
COPY . /myapp
RUN yarn install && yarn build

FROM nginx:alpine as final
COPY --from=0 /myapp/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
