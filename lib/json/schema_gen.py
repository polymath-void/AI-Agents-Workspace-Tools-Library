import json
from pathlib import Path

class JSONSchemaGenerator:
    """
    Infers standard JSON Schema specifications from sample data structures.
    """

    @classmethod
    def infer_schema(cls, value, title="InferredSchema"):
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": title
        }
        schema.update(cls._infer_type_schema(value))
        return schema

    @classmethod
    def _infer_type_schema(cls, val):
        if val is None:
            return {"type": "null"}
        elif isinstance(val, bool):
            return {"type": "boolean"}
        elif isinstance(val, int):
            return {"type": "integer"}
        elif isinstance(val, float):
            return {"type": "number"}
        elif isinstance(val, str):
            return {"type": "string"}
        elif isinstance(val, list):
            if not val:
                return {"type": "array", "items": {}}
            # Infer item schema from first or merged items
            item_schemas = [cls._infer_type_schema(item) for item in val[:5]]
            # If all same type
            first_type = item_schemas[0].get("type")
            if all(s.get("type") == first_type for s in item_schemas):
                return {"type": "array", "items": item_schemas[0]}
            else:
                return {"type": "array", "items": {"anyOf": item_schemas}}
        elif isinstance(val, dict):
            properties = {}
            required = []
            for k, v in val.items():
                properties[k] = cls._infer_type_schema(v)
                required.append(k)
            return {
                "type": "object",
                "properties": properties,
                "required": required
            }
        return {"type": "string"}
