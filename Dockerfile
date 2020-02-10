FROM python:3.7

ADD . /usr/jatm

WORKDIR /usr/jatm

COPY . .

RUN pip install pipenv && pipenv install --system --deploy

EXPOSE 8080:8080

CMD ["python3.7", "main.py"]