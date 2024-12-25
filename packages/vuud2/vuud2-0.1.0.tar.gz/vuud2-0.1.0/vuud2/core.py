
# docker-compose

# services:
#   api:
#     build: ./backend
#     volumes:
#       - ./backend:/app
#     ports:
#       - "8000:8000"
#     depends_on:
#       - dbpg
  
#   dbpg:
#     image: postgres:latest
#     environment:
#       - POSTGRES_USER=postgres
#       - POSTGRES_PASSWORD=postgres
#       - POSTGRESS_DB=postgres


# dockerfile

# FROM python:3.12-slim
# WORKDIR /src
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY . . 
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# psycopg2-binary==2.9.10