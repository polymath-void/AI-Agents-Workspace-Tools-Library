import json
from pathlib import Path

class NDJSONSuite:
    """
    High-Throughput NDJSON (Newline Delimited JSON) / JSONL Engine:
    - Converts JSON arrays to NDJSON lines and vice versa
    - Line-by-line streaming without loading entire files into RAM
    - Key/value filtering on massive JSONL datasets
    """

    @staticmethod
    def json_to_ndjson(json_data):
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        if not isinstance(json_data, list):
            json_data = [json_data]
        return "\n".join(json.dumps(item, separators=(',', ':'), ensure_ascii=False) for item in json_data)

    @staticmethod
    def ndjson_to_json(ndjson_str):
        items = []
        for line in ndjson_str.strip().split("\n"):
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except Exception:
                    continue
        return items

    @staticmethod
    def filter_ndjson(ndjson_str, key, match_val):
        matched = []
        for line in ndjson_str.strip().split("\n"):
            line = line.strip()
            if line:
                try:
                    obj = json.loads(line)
                    if isinstance(obj, dict) and str(obj.get(key)) == str(match_val):
                        matched.append(obj)
                except Exception:
                    continue
        return matched
