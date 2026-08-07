import json
import re

class JSONFilterEngine:
    """
    Predicate Query & Filtering Engine for JSON Array Collections:
    - Supports comparison operators: ==, !=, >, >=, <, <=, contains, startswith, in
    """

    @classmethod
    def filter_array(cls, data, field, operator, expected_val):
        if isinstance(data, str):
            data = json.loads(data)

        if isinstance(data, dict):
            # If root is dict, look for first list in values or wrap
            for v in data.values():
                if isinstance(v, list):
                    data = v
                    break
            if not isinstance(data, list):
                data = [data]

        filtered = []
        for item in data:
            if not isinstance(item, dict):
                continue
            val = cls._get_nested_field(item, field)
            if cls._eval_predicate(val, operator, expected_val):
                filtered.append(item)

        return filtered

    @staticmethod
    def _get_nested_field(item, field_path):
        parts = field_path.split(".")
        curr = item
        for p in parts:
            if isinstance(curr, dict) and p in curr:
                curr = curr[p]
            else:
                return None
        return curr

    @staticmethod
    def _eval_predicate(actual, op, expected):
        if op in ("==", "="):
            return str(actual).lower() == str(expected).lower() if isinstance(actual, bool) else str(actual) == str(expected)
        elif op == "!=":
            return str(actual) != str(expected)
        elif op == ">":
            try:
                return float(actual) > float(expected)
            except (ValueError, TypeError):
                return False
        elif op == ">=":
            try:
                return float(actual) >= float(expected)
            except (ValueError, TypeError):
                return False
        elif op == "<":
            try:
                return float(actual) < float(expected)
            except (ValueError, TypeError):
                return False
        elif op == "<=":
            try:
                return float(actual) <= float(expected)
            except (ValueError, TypeError):
                return False
        elif op == "contains":
            return expected in str(actual) if actual is not None else False
        elif op == "startswith":
            return str(actual).startswith(expected) if actual is not None else False
        return False
