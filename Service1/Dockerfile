FROM python:3.6
WORKDIR /app
COPY . .
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT '/usr/local/bin/python' 'app.py'
