FROM ubuntu

WORKDIR /usr/src/app

COPY . .

RUN apt update
RUN apt-get update && apt-get install -y \
  vim\
  python3 \
  python3-pip


RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install confluent-kafka
RUN python3 -m pip install grpcio
RUN python3 -m pip install grpcio-tools
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. weather.proto

CMD ["python3", "./server.py"]