# Playground for Kafka & Flink

With Flink image supporting python 3.10 ;-;

### Setup
```
cp .env.dev .env
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt -r requirements-dev.txt
make up
```
### Cleanup
```make cleanup```




## UI
Kafka ```localhost:9000```

Flink ```localhost:8081```

## Running ingestor
```make run_ingestor```


## Running aggregator
```make run_aggregator```