FROM python:3.9
WORKDIR "/app"
COPY . .
RUN pip install -r requirements.txt
ENV SECRET_KEY=09f26e402586e2faa8da4c98a35f1b20d6b033c60
ENV MONGO_HOST=localhost
ENV PORT=8000
EXPOSE 8000
CMD ["python3", "main.py"]