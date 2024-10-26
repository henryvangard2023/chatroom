FROM python:3.12

WORKDIR /chatroom

COPY . /chatroom/

CMD ["python", "main.py"]