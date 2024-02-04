FROM python:3.10

WORKDIR /ChatBot

COPY ./requirements.txt /ChatBot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /ChatBot/requirements.txt
RUN mkdir /ChatBot/documents
RUN mkdir /ChatBot/model

COPY ./app /ChatBot/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
