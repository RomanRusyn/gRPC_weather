Weather APP using gRPC
                  Kafka
                  Zookeeper

This APP takes weather for the city

To run the APP use docker :

    * run zookeeper:
        docker run -d\
        --net=host\
        --name=zookeeper\
        --rm\
         -e ZOOKEEPER_CLIENT_PORT=32181\
        confluentinc/cp-zookeeper:4.0.0
    
    * run kafka:
        docker run -d \
        --net=host \
        --name=kafka \
        --rm \
        -e KAFKA_ZOOKEEPER_CONNECT=localhost:32181 \
        -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:29092 \
        -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
        confluentinc/cp-kafka:4.0.0
        
    * In weatherapp folder run:
        docker build -t producer_img .
        
        docker run \
        -it --name producer_cont\
         --net=host \
        --rm \
        producer_img
        
    * In consumer folder run:
        python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. weather.proto
        
        python3 server.py
        
        python3 client.py

