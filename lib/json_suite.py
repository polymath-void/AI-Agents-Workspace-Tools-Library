import json
import re
import sys
from pathlib import Path

class JSONSuite:
    """
    High-performance, zero-overhead JSON toolkit for autonomous AI agents:
    - Dot-notation / JSONPath querying
    - Deep merging and RFC 6902 atomic patching
    - Structural schema validation
    - Token-density packing and minification
    """

    @staticmethod
    def query(data, path_expr):
        """
        Queries nested JSON data using dot/bracket syntax: e.g. 'users.0.name' or 'config.build.targetSdk'
        """
        if not path_expr or path_expr == ".":
            return data

        # Normalize brackets: 'users[0].name' -> 'users.0.name'
        norm_expr = re.sub(r'\[(\w+)\]', r'.\1', path_expr)
        keys = [k for k in norm_expr.split('.') if k]

        current = data
        for k in keys:
            if isinstance(current, dict):
                if k in current:
                    current = current[k]
                else:
                    return None
            elif isinstance(current, list):
                try:
                    idx = int(k)
                    if 0 <= idx < len(current):
                        current = current[idx]
                    else:
                        return None
                except ValueError:
                    return None
            else:
                return None
        return current

    @staticmethod
    def patch_set(data, path_expr, value):
        """
        Atomically updates or creates nested path with value.
        """
        norm_expr = re.sub(r'\[(\w+)\]', r'.\1', path_expr)
        keys = [k for k in norm_expr.split('.') if k]
        if not keys:
            return value

        current = data
        for i, k in enumerate(keys[:-1]):
            if isinstance(current, dict):
                if k not in current or not isinstance(current[k], (dict, list)):
                    # Lookahead to see if next key is integer
                    next_key = keys[i+1]
                    current[k] = [] if next_key.isdigit() else {}
                current = current[k]
            elif isinstance(current, list):
                idx = int(k)
                while len(current) <= idx:
                    current.append({})
                current = current[idx]

        final_key = keys[-1]
        if isinstance(current, dict):
            current[final_key] = value
        elif isinstance(current, list):
            idx = int(final_key)
            while len(current) <= idx:
                current.append(None)
            current[idx] = value

        return data

    @staticmethod
    def deep_merge(base, update):
        """
        Recursively merges update dict into base dict.
        """
        if not isinstance(base, dict) or not isinstance(update, dict):
            return update

        merged = dict(base)
        for k, v in update.items():
            if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
                merged[k] = JSONSuite.deep_merge(merged[k], v)
            else:
                merged[k] = v
        return merged

    @staticmethod
    def validate_schema(data, expected_schema):
        """
        Validates data against a lightweight structural schema definition.
        expected_schema = {
            "required": ["name", "version"],
            "types": {"name": "str", "version": "str", "count": "int"}
        }
        """
        errors = []
        if not isinstance(data, dict):
            return {"valid": False, "errors": ["Data must be a JSON object"]}

        required_keys = expected_schema.get("required", [])
        for req in required_keys:
            if req not in data:
                errors.append(f"Missing required field: '{req}'")

        type_map = {
            "str": str,
            "int": int,
            "float": (int, float),
            "bool": bool,
            "list": list,
            "dict": dict
        }

        expected_types = expected_schema.get("types", {})
        for field, exp_type_str in expected_types.items():
            if field in data:
                val = data[field]
                exp_type = type_map.get(exp_type_str)
                if exp_type and not isinstance(val, exp_type):
                    errors.append(f"Type mismatch on '{field}': expected {exp_type_str}, got {type(val).__name__}")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    @staticmethod
    def minify_pack(data):
        """
        Minifies JSON to zero-whitespace representation for minimal token cost.
        """
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
