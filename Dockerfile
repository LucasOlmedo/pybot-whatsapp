FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY bot/ bot/
COPY bot/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--reload", "--bind", "0.0.0.0:5000", "bot.whatsapp_bot:app"]
