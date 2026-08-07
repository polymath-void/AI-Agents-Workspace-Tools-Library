import json
from collections import Counter

class JSONStatsInspector:
    """
    Deep Structural & Analytical Profiler for JSON Payloads:
    - Calculates maximum depth, key counts, data volume, and token estimates
    - Computes type distributions and null ratios
    """

    @classmethod
    def inspect(cls, data):
        if isinstance(data, str):
            data = json.loads(data)

        stats = {
            "total_keys": 0,
            "max_depth": 0,
            "type_counts": Counter(),
            "null_count": 0,
            "total_values": 0,
            "byte_size": len(json.dumps(data, separators=(',', ':'))),
            "estimated_tokens": max(1, len(json.dumps(data, separators=(',', ':'))) // 4)
        }

        cls._traverse(data, stats, depth=1)
        stats["type_distribution"] = dict(stats.pop("type_counts"))
        return stats

    @classmethod
    def _traverse(cls, node, stats, depth=1):
        if depth > stats["max_depth"]:
            stats["max_depth"] = depth

        if node is None:
            stats["null_count"] += 1
            stats["total_values"] += 1
            stats["type_counts"]["null"] += 1
        elif isinstance(node, bool):
            stats["total_values"] += 1
            stats["type_counts"]["boolean"] += 1
        elif isinstance(node, (int, float)):
            stats["total_values"] += 1
            stats["type_counts"]["number"] += 1
        elif isinstance(node, str):
            stats["total_values"] += 1
            stats["type_counts"]["string"] += 1
        elif isinstance(node, list):
            stats["type_counts"]["array"] += 1
            for item in node:
                cls._traverse(item, stats, depth + 1)
        elif isinstance(node, dict):
            stats["type_counts"]["object"] += 1
            stats["total_keys"] += len(node)
            for k, v in node.items():
                cls._traverse(v, stats, depth + 1)
