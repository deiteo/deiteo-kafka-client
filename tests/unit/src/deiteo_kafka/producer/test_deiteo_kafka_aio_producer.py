import pytest


@pytest.mark.usefixtures("deiteo_kafka_aio_instance")
@pytest.mark.parametrize("input", [{"A": 0}])
def test_produce_dict() -> None:
    pass


@pytest.mark.usefixtures("deiteo_kafka_aio_instance")
def test_produce_str() -> None:
    pass
