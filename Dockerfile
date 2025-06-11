# Usa una imagen oficial de Python
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /code

# Copia los requisitos e instálalos
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia el resto del código
COPY . /code/

# Expone el puerto 80
EXPOSE 80

# Comando para arrancar FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]