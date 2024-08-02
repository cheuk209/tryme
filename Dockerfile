FROM python:3.12
ARG ALPHA_VANTAGE_API_KEY
ENV ALPHA_VANTAGE_API_KEY=$ALPHA_VANTAGE_API_KEY

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./app
COPY ./tests ./tests
EXPOSE 80
CMD ["fastapi", "run", "/app/app/main.py", "--host", "0.0.0.0", "--port", "80"]