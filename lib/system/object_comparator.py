import ast
import json
import hashlib
import re
from pathlib import Path

class ObjectComparator:
    """
    Autonomous Object Identification, Semantic Comparison, and Contract Drift Engine.
    """

    @staticmethod
    def identify_object_type(data_or_code):
        """
        Identifies whether an object is a JSON Schema, Python AST, Kotlin/Java Source, C Header, or Binary/Hash.
        """
        if isinstance(data_or_code, (dict, list)):
            return "DATA_STRUCTURE"

        text = str(data_or_code).strip()

        # Check JSON
        if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
            try:
                json.loads(text)
                return "JSON_OBJECT"
            except Exception:
                pass

        # Check Python AST
        try:
            tree = ast.parse(text)
            if any(isinstance(node, (ast.ClassDef, ast.FunctionDef)) for node in ast.walk(tree)):
                return "PYTHON_CODE_OBJECT"
        except Exception:
            pass

        # Check Kotlin / Java
        if re.search(r'\b(class|interface|object|fun|data class|val|var)\b', text):
            return "KOTLIN_JAVA_OBJECT"

        # Check C/C++ Header
        if re.search(r'\b(struct|typedef|void|int|extern|JNIEXPORT)\b', text):
            return "NATIVE_C_OBJECT"

        return "RAW_TEXT_OR_BINARY"

    @staticmethod
    def extract_symbols(code_content, language="auto"):
        """
        Extracts named code entities (classes, methods, fields, functions) and their signatures.
        """
        symbols = {
            "classes": [],
            "functions": [],
            "properties": []
        }

        # Try Python AST extraction
        try:
            tree = ast.parse(code_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    symbols["classes"].append({"name": node.name, "methods": methods, "line": node.lineno})
                elif isinstance(node, ast.FunctionDef) and not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree) if node in getattr(parent, 'body', [])):
                    args = [a.arg for a in node.args.args]
                    symbols["functions"].append({"name": node.name, "args": args, "line": node.lineno})
            if symbols["classes"] or symbols["functions"]:
                return symbols
        except Exception:
            pass

        # Fallback / Kotlin / Java Regex extraction
        class_matches = re.finditer(r'(?:class|interface|object|data class)\s+([A-Za-z0-9_]+)', code_content)
        for m in class_matches:
            symbols["classes"].append({"name": m.group(1), "methods": []})

        fun_matches = re.finditer(r'(?:fun|def|void|int|suspend fun)\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)', code_content)
        for m in fun_matches:
            symbols["functions"].append({"name": m.group(1), "args": m.group(2).strip()})

        prop_matches = re.finditer(r'(?:val|var)\s+([A-Za-z0-9_]+)', code_content)
        for m in prop_matches:
            symbols["properties"].append(m.group(1))

        return symbols

    @staticmethod
    def compare_json_objects(obj1, obj2, path=""):
        """
        Performs deep structural and value comparison of two JSON/Dict objects.
        Returns: { 'added': [...], 'removed': [...], 'type_mismatches': [...], 'value_diffs': [...] }
        """
        diff = {
            "added": [],
            "removed": [],
            "type_mismatches": [],
            "value_diffs": []
        }

        if isinstance(obj1, dict) and isinstance(obj2, dict):
            keys1 = set(obj1.keys())
            keys2 = set(obj2.keys())

            for k in keys2 - keys1:
                diff["added"].append(f"{path}.{k}" if path else k)

            for k in keys1 - keys2:
                diff["removed"].append(f"{path}.{k}" if path else k)

            for k in keys1 & keys2:
                sub_path = f"{path}.{k}" if path else k
                v1, v2 = obj1[k], obj2[k]
                if type(v1) != type(v2):
                    diff["type_mismatches"].append({
                        "key": sub_path,
                        "expected_type": type(v1).__name__,
                        "actual_type": type(v2).__name__
                    })
                elif isinstance(v1, (dict, list)):
                    sub_diff = ObjectComparator.compare_json_objects(v1, v2, path=sub_path)
                    for k_sub in ["added", "removed", "type_mismatches", "value_diffs"]:
                        diff[k_sub].extend(sub_diff[k_sub])
                elif v1 != v2:
                    diff["value_diffs"].append({
                        "key": sub_path,
                        "old_value": v1,
                        "new_value": v2
                    })

        elif isinstance(obj1, list) and isinstance(obj2, list):
            if len(obj1) != len(obj2):
                diff["value_diffs"].append({
                    "key": f"{path}[length]",
                    "old_value": len(obj1),
                    "new_value": len(obj2)
                })
            for idx, (item1, item2) in enumerate(zip(obj1, obj2)):
                sub_path = f"{path}[{idx}]"
                sub_diff = ObjectComparator.compare_json_objects(item1, item2, path=sub_path)
                for k_sub in ["added", "removed", "type_mismatches", "value_diffs"]:
                    diff[k_sub].extend(sub_diff[k_sub])
        elif obj1 != obj2:
            diff["value_diffs"].append({"key": path, "old_value": obj1, "new_value": obj2})

        return diff

    @staticmethod
    def compare_code_entities(code1, code2):
        """
        Compares two code files or snippets at the symbol level (classes, functions, signatures).
        """
        sym1 = ObjectComparator.extract_symbols(code1)
        sym2 = ObjectComparator.extract_symbols(code2)

        classes1 = {c["name"]: c for c in sym1["classes"]}
        classes2 = {c["name"]: c for c in sym2["classes"]}

        funcs1 = {f["name"]: f for f in sym1["functions"]}
        funcs2 = {f["name"]: f for f in sym2["functions"]}

        report = {
            "classes_added": list(set(classes2.keys()) - set(classes1.keys())),
            "classes_removed": list(set(classes1.keys()) - set(classes2.keys())),
            "functions_added": list(set(funcs2.keys()) - set(funcs1.keys())),
            "functions_removed": list(set(funcs1.keys()) - set(funcs2.keys())),
            "signature_changes": []
        }

        # Check signature drift on common functions
        for f_name in set(funcs1.keys()) & set(funcs2.keys()):
            a1 = funcs1[f_name].get("args")
            a2 = funcs2[f_name].get("args")
            if a1 != a2:
                report["signature_changes"].append({
                    "function": f_name,
                    "old_args": a1,
                    "new_args": a2
                })

        return report
