# 1. Usar una imagen oficial de Python ligera como base
FROM python:3.14.3-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar primero el archivo de dependencias
# Esto ayuda a que Docker cachee (guarde en memoria) este paso y sea más rápido en el futuro
COPY requirements.txt .

# 4. Instalar Flask (que es lo único que pusimos en requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto de tus archivos (tu app.py y la carpeta templates) al contenedor
COPY . .

# 6. Exponer el puerto 5000, que es el que usaste en app.run(port=5000)
EXPOSE 5000

# 7. El comando final para arrancar tu aplicación cuando se encienda el contenedor
CMD ["python", "app.py"]