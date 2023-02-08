FROM python:3.8-slim

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

COPY . .
CMD ["python", "-u", "main.py"]
