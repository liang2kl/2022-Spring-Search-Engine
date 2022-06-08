FROM node:latest as build

ENV HOME=/opt/app

WORKDIR $HOME
COPY . $HOME

RUN npm config set registry http://mirrors.cloud.tencent.com/npm/ \
    && npm install \
    && npm run build

FROM nginx:1.19

COPY --from=build /opt/app/build /usr/share/nginx/html
COPY --from=build /opt/app/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
