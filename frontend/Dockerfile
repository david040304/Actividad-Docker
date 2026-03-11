# ── Frontend image (Nginx) ─────────────────────────────
FROM nginx:1.27-alpine

# Eliminar la config por defecto de nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiar nuestra config personalizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar archivos estáticos
COPY public/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
