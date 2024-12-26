import json
from jsonschema import ValidationError, validate
from nats.aio.client import Client as NATS
from event_schema import event_schema

nc = NATS()


async def connect_nats(server_url):
    if not server_url:
        raise ValueError("NATS server URL is not provided")
    if not nc.is_connected:
        await nc.connect(servers=[server_url])


# Helper function to publish NATS event
async def publish_event(subject, data):
    try:
        validate(instance=data, schema=event_schema)
    except ValidationError as e:
        raise ValidationError(f"Validation failed: {e.message}")

    # Serialize the event data to JSON
    event_json = json.dumps(data).encode("utf-8")

    if nc.is_connected:
        await nc.publish(subject, event_json)
    else:
        raise ConnectionError("NATS connection is not established")
