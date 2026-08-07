import json
import re
from pathlib import Path

class PromptJSONProcessor:
    """
    Handles unformatted / noisy user prompts:
    - Extracts embedded JSON objects/arrays from mixed natural language text
    - Auto-repairs malformed JSON (single quotes, trailing commas, unquoted keys)
    - Normalizes unstructured user prompts into actionable intent schemas
    - Dynamically prunes and adjusts workspace context based on prompt query relevance
    """

    @staticmethod
    def repair_json_string(raw_text):
        """
        Attempts heuristic repairs on malformed JSON strings.
        """
        text = raw_text.strip()

        # Remove markdown code block markers
        text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'```$', '', text, flags=re.MULTILINE).strip()

        # Replace single quotes with double quotes (ignoring escaped ones)
        # First check if standard JSON parse works
        try:
            return json.loads(text)
        except Exception:
            pass

        # Heuristic 1: Replace single quotes with double quotes
        repaired = re.sub(r"'([^']*)'", r'"\1"', text)

        # Heuristic 2: Remove trailing commas before } or ]
        repaired = re.sub(r',\s*([}\]])', r'\1', repaired)

        # Heuristic 3: Quote unquoted object keys (e.g. {name: "val"} -> {"name": "val"})
        repaired = re.sub(r'([{,]\s*)([A-Za-z0-9_]+)\s*:', r'\1"\2":', repaired)

        # Heuristic 4: Replace Python/JS literals True/False/None/undefined
        repaired = re.sub(r'\bTrue\b', 'true', repaired)
        repaired = re.sub(r'\bFalse\b', 'false', repaired)
        repaired = re.sub(r'\bNone\b', 'null', repaired)
        repaired = re.sub(r'\bundefined\b', 'null', repaired)

        try:
            return json.loads(repaired)
        except Exception as e:
            return None

    @staticmethod
    def extract_json_from_prompt(prompt_text):
        """
        Scans unformatted prompt text for embedded JSON payloads and parses them.
        """
        # 1. First check for ```json ... ``` blocks
        code_blocks = re.findall(r'```(?:json)?\s*([\s\S]*?)```', prompt_text)
        for block in code_blocks:
            parsed = PromptJSONProcessor.repair_json_string(block)
            if parsed is not None:
                return parsed

        # 2. Heuristic scan for outermost { ... } or [ ... ]
        first_brace = prompt_text.find('{')
        last_brace = prompt_text.rfind('}')
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            candidate = prompt_text[first_brace:last_brace+1]
            parsed = PromptJSONProcessor.repair_json_string(candidate)
            if parsed is not None:
                return parsed

        first_bracket = prompt_text.find('[')
        last_bracket = prompt_text.rfind(']')
        if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
            candidate = prompt_text[first_bracket:last_bracket+1]
            parsed = PromptJSONProcessor.repair_json_string(candidate)
            if parsed is not None:
                return parsed

        return None

    @staticmethod
    def normalize_prompt_intent(prompt_text):
        """
        Extracts structured intent, action type, target entities, and parameters from unstructured user prompt.
        """
        prompt_lower = prompt_text.lower()
        extracted_json = PromptJSONProcessor.extract_json_from_prompt(prompt_text)

        intent = {
            "raw_prompt": prompt_text,
            "detected_action": "GENERAL_QUERY",
            "parameters": {},
            "embedded_payload": extracted_json
        }

        # Classify intent actions
        if any(w in prompt_lower for w in ["build", "compile", "gradle", "doctor", "fix build"]):
            intent["detected_action"] = "BUILD_REPAIR"
        elif any(w in prompt_lower for w in ["refactor", "replace", "change", "modify", "rename"]):
            intent["detected_action"] = "CODE_REFACTOR"
        elif any(w in prompt_lower for w in ["compare", "diff", "identify", "difference"]):
            intent["detected_action"] = "OBJECT_DIFF"
        elif any(w in prompt_lower for w in ["pack", "bundle", "package", "release"]):
            intent["detected_action"] = "BUNDLE_PACK"
        elif any(w in prompt_lower for w in ["search", "find", "locate", "where"]):
            intent["detected_action"] = "WORKSPACE_SEARCH"
        elif any(w in prompt_lower for w in ["crash", "stacktrace", "logcat", "error", "sigsegv"]):
            intent["detected_action"] = "CRASH_DIAGNOSTICS"
        elif any(w in prompt_lower for w in ["dag", "workflow", "parallel", "subtask", "mesh"]):
            intent["detected_action"] = "WORKFLOW_ORCHESTRATION"

        # Parameter extraction heuristics
        # Extract target paths
        paths = re.findall(r'(?:(?:/[\w\.-]+)+|(?:[\w\.-]+/[/\w\.-]+)|(?:[A-Za-z0-9_\-]+\.(?:kt|java|py|json|c|h|xml|gradle)))', prompt_text)
        if paths:
            intent["parameters"]["referenced_files"] = list(set(paths))

        return intent

    @staticmethod
    def adjust_context(prompt_text, available_snippets, max_snippets=5):
        """
        Dynamically adjusts context by ranking available code/doc snippets by relevance to the prompt.
        """
        prompt_tokens = set(re.findall(r'\w+', prompt_text.lower()))
        
        scored = []
        for item in available_snippets:
            title = item.get("title", "")
            content = item.get("content", "")
            tokens = set(re.findall(r'\w+', (title + " " + content).lower()))
            overlap = len(prompt_tokens & tokens)
            scored.append((overlap, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored[:max_snippets] if score > 0]
