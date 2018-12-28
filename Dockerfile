FROM python:3.6
LABEL maintainer "Zbigniew Michna"
WORKDIR /app
COPY . /app
RUN pip install -r ./api/requirements.txt
EXPOSE 5090
CMD ["python", "server.py"]