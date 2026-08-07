"""
Dedicated Python AST, Code Modification, Scaffolding, and Runtime Inspection Suite for AI Agents.
"""
from .analyzer import ComplexityAnalyzer, analyze_workspace, workspace_summary
from .code_modder import batch_code_replace, inject_import
from .scaffolder import scaffold_compose_component, scaffold_repository
from .env_checker import get_system_telemetry, get_installed_toolchains
from .crash_doctor import parse_stacktrace
from .electron_runner import ElectronStudioRunner

__all__ = [
    "ComplexityAnalyzer", "analyze_workspace", "workspace_summary",
    "batch_code_replace", "inject_import",
    "scaffold_compose_component", "scaffold_repository",
    "get_system_telemetry", "get_installed_toolchains",
    "parse_stacktrace", "ElectronStudioRunner"
]

