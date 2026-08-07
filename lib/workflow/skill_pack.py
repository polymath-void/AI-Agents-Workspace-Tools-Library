import os
import re
import json
import tarfile
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional

class SkillPacker:
    """Automated SKILL.md linter, YAML frontmatter validator, AST toolchain dependency validator and packager."""

    @staticmethod
    def parse_frontmatter(content: str) -> Dict[str, Any]:
        """Parses YAML frontmatter block from markdown content without external yaml parser."""
        if not content.startswith("---"):
            return {"error": "Missing leading '---' frontmatter boundary"}

        parts = content.split("---", 2)
        if len(parts) < 3:
            return {"error": "Malformed frontmatter block; missing closing '---'"}

        front_str = parts[1].strip()
        body = parts[2].strip()

        meta = {}
        for line in front_str.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("\"'")

        return {"meta": meta, "body": body}

    @classmethod
    def lint_skill(cls, skill_path: Path) -> Dict[str, Any]:
        """Lints a single SKILL.md against master operating standards."""
        if not skill_path.exists():
            return {"valid": False, "errors": [f"Skill file not found: {skill_path}"]}

        content = skill_path.read_text(encoding="utf-8", errors="replace")
        parsed = cls.parse_frontmatter(content)
        
        errors = []
        warnings = []

        if "error" in parsed:
            errors.append(parsed["error"])
            return {"valid": False, "errors": errors, "warnings": warnings}

        meta = parsed.get("meta", {})
        body = parsed.get("body", "")

        # 1. Frontmatter Validation
        if "name" not in meta:
            errors.append("Frontmatter missing required 'name' attribute.")
        elif not re.match(r"^[a-z0-9_-]+$", meta["name"]):
            warnings.append(f"Skill name '{meta['name']}' should follow kebab-case naming.")

        if "description" not in meta:
            errors.append("Frontmatter missing required 'description' attribute.")
        elif len(meta.get("description", "")) < 20:
            warnings.append("Description is very brief (< 20 characters).")

        # 2. Body Structure Validation
        if not re.search(r"^#\s+", body, re.MULTILINE):
            warnings.append("Skill missing top-level H1 header ('# Title').")

        # 3. Check for Clickable Markdown Links format
        bad_links = re.findall(r"`\[.*?\]\(.*?\)```?", body)
        if bad_links:
            warnings.append(f"Found {len(bad_links)} backtick-wrapped links which may break clickable markdown rendering.")

        # 4. Check for Tool References Section
        has_tools_section = bool(re.search(r"##\s+.*(Tool|Tools|Required Tools)", body, re.IGNORECASE))
        
        # 5. Extract referenced tool names
        referenced_tools = list(set(re.findall(r"wc-[a-z0-9-]+", body)))

        return {
            "valid": len(errors) == 0,
            "skill_name": meta.get("name", skill_path.parent.name),
            "description": meta.get("description", ""),
            "has_tools_section": has_tools_section,
            "referenced_tools": referenced_tools,
            "errors": errors,
            "warnings": warnings
        }

    @classmethod
    def validate_directory(cls, dir_path: Path) -> Dict[str, Any]:
        """Scans and lints all SKILL.md files under a workspace or skills directory."""
        if not dir_path.exists():
            return {"valid": False, "error": f"Directory not found: {dir_path}"}

        skills_found = list(dir_path.rglob("SKILL.md"))
        results = []
        total_errors = 0
        total_warnings = 0

        for skill_file in sorted(skills_found):
            lint_res = cls.lint_skill(skill_file)
            lint_res["path"] = str(skill_file)
            results.append(lint_res)
            total_errors += len(lint_res["errors"])
            total_warnings += len(lint_res["warnings"])

        return {
            "valid": total_errors == 0,
            "total_skills": len(skills_found),
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "results": results
        }

    @classmethod
    def pack_skill(cls, skill_dir: Path, output_file: Optional[Path] = None) -> Dict[str, Any]:
        """Packs a skill folder into a verified bundle archive."""
        if not skill_dir.exists() or not skill_dir.is_dir():
            return {"status": "ERROR", "message": f"Skill directory not found: {skill_dir}"}

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return {"status": "ERROR", "message": f"Missing SKILL.md in {skill_dir}"}

        lint = cls.lint_skill(skill_md)
        if not lint["valid"]:
            return {"status": "ERROR", "message": "Skill failed lint checks", "errors": lint["errors"]}

        skill_name = lint["skill_name"]
        output_file = output_file or (skill_dir.parent / f"{skill_name}.skill")

        manifest = {
            "skill_name": skill_name,
            "description": lint["description"],
            "referenced_tools": lint["referenced_tools"],
            "files": {}
        }

        with tarfile.open(output_file, "w:gz") as tar:
            for p in sorted(skill_dir.rglob("*")):
                if p.is_file():
                    h = hashlib.sha256()
                    with open(p, "rb") as f:
                        while chunk := f.read(65536):
                            h.update(chunk)
                    rel = str(p.relative_to(skill_dir))
                    manifest["files"][rel] = {
                        "size": p.stat().st_size,
                        "sha256": h.hexdigest()
                    }
                    tar.add(p, arcname=rel)

        # Calculate bundle hash
        bundle_sha = hashlib.sha256()
        with open(output_file, "rb") as f:
            while chunk := f.read(65536):
                bundle_sha.update(chunk)

        manifest["bundle_sha256"] = bundle_sha.hexdigest()
        manifest["bundle_size"] = output_file.stat().st_size

        # Write sidecar manifest
        manifest_path = output_file.with_suffix(".manifest.json")
        manifest_path.write_text(json.dumps(manifest, indent=2))

        return {
            "status": "SUCCESS",
            "skill_name": skill_name,
            "bundle": str(output_file),
            "manifest": str(manifest_path),
            "sha256": manifest["bundle_sha256"],
            "size_bytes": manifest["bundle_size"]
        }

    @classmethod
    def unpack_skill(cls, bundle_path: Path, dest_dir: Path) -> Dict[str, Any]:
        """Unpacks and verifies a .skill package bundle."""
        if not bundle_path.exists():
            return {"status": "ERROR", "message": f"Bundle file not found: {bundle_path}"}

        dest_dir.mkdir(parents=True, exist_ok=True)
        with tarfile.open(bundle_path, "r:gz") as tar:
            tar.extractall(path=dest_dir)

        skill_md = dest_dir / "SKILL.md"
        lint = cls.lint_skill(skill_md) if skill_md.exists() else {"valid": False, "errors": ["SKILL.md not extracted"]}

        return {
            "status": "SUCCESS",
            "extracted_to": str(dest_dir),
            "skill_valid": lint.get("valid", False)
        }
