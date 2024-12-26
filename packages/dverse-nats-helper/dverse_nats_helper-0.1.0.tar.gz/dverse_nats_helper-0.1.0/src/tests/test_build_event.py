from dverse_nats_helper.example_models import Base
import pytest
from sqlalchemy import create_engine
from dverse_nats_helper.event_builder import build_event
from dverse_nats_helper.example_models import Product, User
from sqlalchemy.orm import sessionmaker
import uuid
import inspect


@pytest.fixture
def sample_system():
    return {
        "event_type": "object_created",
        "platform": "example_platform",
        "service": "example_service",
    }


@pytest.fixture
def sample_actor():
    return {
        "actor_id": "12345",
        "username": "test_user",
    }


@pytest.fixture(scope="module")
def test_session():
    engine = create_engine("sqlite:///:memory:")  # In-memory SQLite database
    Base.metadata.create_all(engine)  # Create tables
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def custom_message_structure_for(object):
    print(f"DEBUG: Object attributes: {inspect.getmembers(object)}")
    if isinstance(object, Product):
        ...


def test_build_event_with_valid_product():
    product = Product(id=uuid.uuid4(), title="Test Product", price=100.0)
    actor = {"actor_id": "user123", "username": "testuser"}
    system = {
        "event_type": "object_created",
        "platform": "example_platform",
        "service": "example_service",
    }

    event = build_event(product, actor, system)

    assert event["object"]["product_id"] == str(product.id)
    assert event["event_type"] == "object_created"


def test_build_event_with_invalid_object():
    class InvalidObject:
        pass

    invalid_object = InvalidObject()
    actor = {"actor_id": "user123", "username": "testuser"}
    system = {
        "event_type": "object_created",
        "platform": "example_platform",
        "service": "example_service",
    }

    with pytest.raises(ValueError, match="Unsupported object type"):
        build_event(invalid_object, actor, system)


def test_build_event_with_product(sample_system, sample_actor, test_session):
    product = Product(id=uuid.uuid4(), title="Sample Product", price=19.99)
    test_session.add(product)
    test_session.commit()

    event = build_event(product, sample_actor, sample_system)

    assert event["object"]["product_id"] == str(product.id)
    assert event["object"]["title"] == "Sample Product"
    assert event["object"]["price"] == "19.99"


def test_build_event_with_user(sample_system, sample_actor):
    user = User(id=1, username="test_user")

    event = build_event(user, sample_actor, sample_system)

    assert event["object"]["user_id"] == "1"
    assert event["object"]["username"] == "test_user"
