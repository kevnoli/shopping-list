FROM node:18 as builder
WORKDIR /code
COPY ./frontend/package*.json .
RUN npm install
COPY ./frontend/ .
CMD npm run build

FROM nginx
ARG BUILD=dev
COPY ./default-${BUILD}.conf /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/nginx.conf
WORKDIR /usr/share/nginx/html/
RUN rm -f *
COPY --from=builder /code/dist .