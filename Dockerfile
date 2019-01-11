FROM python:3.6
LABEL maintainer="Zbigniew Michna"
COPY ./api/requirements.txt /
RUN pip install -r requirements.txt	
WORKDIR /app
COPY . /app
ENV DB_NAME=postgres
ENV DB_USER=postgres
ENV DB_PASS=postgres
ENV DB_SERVICE=postgres
ENV DB_PORT=5432
EXPOSE 5090
CMD ["python", "server.py"]