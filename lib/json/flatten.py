import json

class JSONFlattener:
    """
    Bidirectional JSON Hierarchical Flattener & Unflattener:
    - Flattens deep nested dicts/lists into single-level dot keys (e.g. {"a.b.0.c": 42})
    - Restores deep nested hierarchies from flat dot-notated objects
    """

    @classmethod
    def flatten(cls, data, delimiter=".", prefix=""):
        flat = {}
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{prefix}{delimiter}{k}" if prefix else str(k)
                if isinstance(v, (dict, list)) and v:
                    flat.update(cls.flatten(v, delimiter=delimiter, prefix=new_key))
                else:
                    flat[new_key] = v
        elif isinstance(data, list):
            for i, v in enumerate(data):
                new_key = f"{prefix}{delimiter}{i}" if prefix else str(i)
                if isinstance(v, (dict, list)) and v:
                    flat.update(cls.flatten(v, delimiter=delimiter, prefix=new_key))
                else:
                    flat[new_key] = v
        else:
            flat[prefix] = data
        return flat

    @classmethod
    def unflatten(cls, flat_data, delimiter="."):
        root = {}
        for flat_key, val in flat_data.items():
            parts = flat_key.split(delimiter)
            curr = root
            for i, part in enumerate(parts[:-1]):
                next_part = parts[i + 1]
                is_next_digit = next_part.isdigit()

                if part.isdigit():
                    part_idx = int(part)
                    while len(curr) <= part_idx:
                        curr.append({} if not is_next_digit else [])
                    curr = curr[part_idx]
                else:
                    if part not in curr:
                        curr[part] = [] if is_next_digit else {}
                    curr = curr[part]

            last_part = parts[-1]
            if last_part.isdigit():
                idx = int(last_part)
                while len(curr) <= idx:
                    curr.append(None)
                curr[idx] = val
            else:
                curr[last_part] = val

        return root
