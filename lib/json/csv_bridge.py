import csv
import io
import json

class JSONCSVBridge:
    """
    Bidirectional Zero-Dependency JSON <-> CSV / TSV Converter:
    - Converts JSON records to standard CSV / TSV strings
    - Parses CSV / TSV tabular data into structured JSON objects with auto-typed numbers and booleans
    """

    @staticmethod
    def json_to_csv(data, delimiter=","):
        if isinstance(data, str):
            data = json.loads(data)
        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list) or not data:
            return ""

        # Collect all unique headers across all records
        headers = []
        for item in data:
            if isinstance(item, dict):
                for k in item.keys():
                    if k not in headers:
                        headers.append(k)

        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=headers, delimiter=delimiter)
        writer.writeheader()
        for row in data:
            if isinstance(row, dict):
                writer.writerow(row)
        return out.getvalue().strip()

    @staticmethod
    def csv_to_json(csv_str, delimiter=","):
        inp = io.StringIO(csv_str.strip())
        reader = csv.DictReader(inp, delimiter=delimiter)
        records = []
        for row in reader:
            parsed_row = {}
            for k, v in row.items():
                if v is None:
                    parsed_row[k] = None
                elif v.lower() == "true":
                    parsed_row[k] = True
                elif v.lower() == "false":
                    parsed_row[k] = False
                elif v.lower() in ("null", "none"):
                    parsed_row[k] = None
                else:
                    try:
                        if "." in v:
                            parsed_row[k] = float(v)
                        else:
                            parsed_row[k] = int(v)
                    except ValueError:
                        parsed_row[k] = v
            records.append(parsed_row)
        return records
