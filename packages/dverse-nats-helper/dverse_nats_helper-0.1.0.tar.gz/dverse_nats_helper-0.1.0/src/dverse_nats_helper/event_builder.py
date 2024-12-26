import uuid
from datetime import datetime, timezone
from jsonschema import ValidationError, validate
from event_schema import event_schema


def build_event(object, actor, system):
    """
    Build an event message conforming to the event schema.

    Args:
        object (dict): A dictionary representing the object.
        actor (dict): A dictionary containing actor details.
        system (dict): A dictionary containing system details.

    Returns:
        dict: The event message.
    """
    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": system["platform"],
        "service": system["service"],
        "event_type": system["event_type"],
        "actor": {
            "actor_id": actor["actor_id"],
            "username": actor["username"],
        },
        "object": custom_message_structure_for(object),
    }

    # Validate the event against the schema
    try:
        validate(instance=event, schema=event_schema)
    except ValidationError as e:
        raise ValueError(f"Event validation failed: {e.message}")

    return event


def custom_message_structure_for(object):
    try:
        return object.to_event_object()
    except AttributeError:
        raise ValueError(f"Unsupported object type: {type(object)}")
