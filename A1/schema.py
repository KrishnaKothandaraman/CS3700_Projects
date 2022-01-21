start_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "id": {"type": "string"}
    }
}

retry_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "id": {"type": "string"},
        "guesses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "word": {"type": "string"},
                    "marks": {
                        "type": "array",
                        "items": {"type": "number"}
                    }
                }
            }

        }
    }
}

bye_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "id": {"type": "string"},
        "flag" : {"type" : "string"}
    }
}
