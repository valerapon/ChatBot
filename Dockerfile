FROM python:3.12.1

WORKDIR /ChatBot

COPY ./requirements.txt /ChatBot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /ChatBot/requirements.txt

COPY ./app /ChatBot/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
