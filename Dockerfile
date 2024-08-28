FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

CMD [ "python3", "main.py" ]
