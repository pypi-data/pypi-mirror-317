event_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "title": "EventMessage",
    "type": "object",
    "required": [
        "event_id",
        "timestamp",
        "platform",
        "service",
        "event_type",
        "actor",
        "object",
    ],
    "properties": {
        "event_id": {
            "type": "string",
            "description": "Unique identifier for the event, typically a UUID",
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "Timestamp in ISO 8601 format (e.g., 2024-11-13T12:34:56Z)",
        },
        "platform": {
            "type": "string",
            "description": (
                "Name of the platform generating the event "
                "(e.g., LineVerse, MarketPlace)"
            ),
        },
        "service": {
            "type": "string",
            "description": "Name of the service within the platform (e.g., auth)",
        },
        "event_type": {
            "type": "string",
            "description": (
                "Type of event (e.g., post, chat, like, share, buy), "
                "representing the action taken"
            ),
        },
        "actor": {
            "type": "object",
            "description": "Details about the user or entity that triggered the event",
            "required": ["actor_id", "username"],
            "properties": {
                "actor_id": {
                    "type": "string",
                    "description": (
                        "Unique identifier for the actor (user or system) "
                        "performing the action"
                    ),
                },
                "username": {"type": "string", "description": "Username of the actor"},
                "email": {
                    "type": "string",
                    "format": "email",
                    "description": "Email address of the actor (optional)",
                },
            },
        },
        "object": {
            "type": "object",
            "description": "Object related to the event (e.g., a specific post)",
            "additionalProperties": True,
        },
    },
}
