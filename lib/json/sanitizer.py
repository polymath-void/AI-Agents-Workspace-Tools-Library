import json
import re
import copy

class JSONSanitizer:
    """
    Automated Security, Secret Masking & PII Redactor for JSON structures:
    - Scans keys and values for sensitive patterns (passwords, tokens, keys, secret, auth, emails)
    - Replaces sensitive tokens with redacted masks (e.g. '***REDACTED***')
    """

    SENSITIVE_KEY_PATTERNS = [
        r"pass(word)?", r"secret", r"token", r"api_?key", r"auth(orization)?",
        r"private_?key", r"cert(ificate)?", r"credential", r"ssn"
    ]

    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    @classmethod
    def sanitize(cls, data, mask="***REDACTED***"):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                return cls.EMAIL_PATTERN.sub(mask, data)

        data_copy = copy.deepcopy(data)
        return cls._mask_node(data_copy, mask)

    @classmethod
    def _mask_node(cls, node, mask):
        if isinstance(node, dict):
            for k, v in node.items():
                if any(re.search(pat, k, re.IGNORECASE) for pat in cls.SENSITIVE_KEY_PATTERNS):
                    node[k] = mask
                elif isinstance(v, (dict, list)):
                    node[k] = cls._mask_node(v, mask)
                elif isinstance(v, str):
                    node[k] = cls.EMAIL_PATTERN.sub(mask, v)
        elif isinstance(node, list):
            for i in range(len(node)):
                if isinstance(node[i], (dict, list)):
                    node[i] = cls._mask_node(node[i], mask)
                elif isinstance(node[i], str):
                    node[i] = cls.EMAIL_PATTERN.sub(mask, node[i])
        return node
