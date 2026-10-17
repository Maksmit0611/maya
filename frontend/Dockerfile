# syntax=docker/dockerfile:1
FROM node:22-alpine AS build
WORKDIR /src
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
ARG VITE_API_BASE_URL=http://localhost:8000
ARG VITE_SUPABASE_URL=
ARG VITE_SUPABASE_PUBLISHABLE_KEY=
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL} \
    VITE_SUPABASE_URL=${VITE_SUPABASE_URL} \
    VITE_SUPABASE_PUBLISHABLE_KEY=${VITE_SUPABASE_PUBLISHABLE_KEY}
RUN npm run build

FROM nginx:1.29-alpine AS runtime
RUN addgroup -S -g 1001 appgroup \
    && adduser -S -D -H -u 1001 -G appgroup appuser \
    && mkdir -p /var/cache/nginx /tmp/nginx \
    && chown -R 1001:1001 /var/cache/nginx /tmp/nginx /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build --link --chown=1001:1001 /src/dist /usr/share/nginx/html
USER 1001:1001
EXPOSE 8080
LABEL org.opencontainers.image.title="MAYA frontend"
CMD ["nginx", "-g", "daemon off;"]
