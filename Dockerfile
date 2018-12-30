FROM python:3.6
LABEL maintainer="Zbigniew Michna"
COPY ./api/requirements.txt /
RUN pip install -r requirements.txt	
WORKDIR /app
COPY . /app
EXPOSE 5090
CMD ["python", "server.py"]