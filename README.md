# Deiteo Kafka Client

A library creating an interface on top of `AIOKafkaProducer`. To handle specific needs of
projects within open source Deiteo organisation.

## Library Usage


### DeiteoKafkaAioProducer
* The `produce` method will accept topic content of type `str` or `Dict[str, Any]`, and will
convert this into a `byte string` to produce to topic.
* The `DeiteoKafkaAioProducer` will create its own event `loop`, or you can inject one.


#### Without providing loop
```python
from deiteo_kafka.producer.deiteo_kafka_aio_producer import DeiteoKafkaAioProducer

bootstrap_servers = "localhost:1234"
topic = "deiteo-input-feed"

topic_content = {"A": 0, "B": "a-string", "C": 0.1}
deiteo_kafka_aio_producer = DeiteoKafkaAioProducer(
    bootstrap_servers=bootstrap_servers,
    topic=topic,
)
await deiteo_kafka_aio_producer.start_producer()
await deiteo_kafka_aio_producer.produce(topic_content=topic_content)
```

#### Providing loop
```python
import asyncio
from deiteo_kafka.producer.deiteo_kafka_aio_producer import DeiteoKafkaAioProducer

loop = asyncio.get_event_loop()
bootstrap_servers = "localhost:1234"
topic = "deiteo-input-feed"

topic_content = {"A": 0, "B": "a-string", "C": 0.1}
deiteo_kafka_aio_producer = DeiteoKafkaAioProducer(
    bootstrap_servers=bootstrap_servers,
    topic=topic,
    loop=loop,
)
await deiteo_kafka_aio_producer.start_producer()
await deiteo_kafka_aio_producer.produce(topic_content=topic_content)
```

You can then stop the producer if needed by:

```python
await deiteo_kafka_aio_producer.stop_producer()
```

This will not stop the event `loop`. If you also want to stop the event loop, simply provide key
`stop_loop=True`.

```python
await deiteo_kafka_aio_producer.stop_producer(stop_loop=True)
```

The reason for this is that you might have a larger application, utilising this `loop`, and you
only want to close the `DeiteoKafkaAioProducer`, but not the event loop itself.

## Setup From Scratch

### Requirement

* ^python3.8
* poetry 1.1.13
* make (GNU Make 3.81)

### Setup

```bash
make setup-environment
```

Update package
```bash
make update
```

### Test

```bash
make test type=unit/integration
```

### Docker

The reason `docker` is used in the source code here, is to be able to build up an encapsulated
environment of the codebase, and do `unit/integration and load tests`.

```bash
make build-container-image
```

```bash
make get-container-info-environment
make run-container-tests type=unit
```
