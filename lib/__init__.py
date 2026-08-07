"""
AI Agents Workspace Tools Library
Modular architecture separating Python AST/Runtime, JSON/Data, Workflows, and System Context.
"""

from . import json
from . import py
from . import workflow
from . import system

# Direct exports for convenience
from .json.json_suite import JSONSuite
from .py.analyzer import ComplexityAnalyzer, analyze_workspace, workspace_summary
from .py.code_modder import batch_code_replace, inject_import
from .py.scaffolder import scaffold_compose_component, scaffold_repository
from .py.env_checker import get_system_telemetry, get_installed_toolchains
from .py.crash_doctor import parse_stacktrace
from .workflow.task_dag import TaskDAG
from .workflow.agent_mesh import AgentMesh
from .workflow.agent_channel import AgentChannel
from .workflow.agent_loop import run_agent_loop
from .workflow.agent_probe import probe_agent_environment
from .workflow.agent_memory import AgentMemoryStore
from .workflow.context_pack import compress_log_trace, pack_agent_context
from .workflow.error_healer import auto_heal_error, ensure_path_configured
from .workflow.resource_lock import ResourceLock
from .system.scanner import scan_directory
from .system.manager import sanitize_workspace
from .system.fast_finder import fast_search
from .system.dep_inspector import inspect_dependencies
from .system.git_helper import get_git_status, sync_branches
from .system.contract_validator import validate_jni_contracts
from .system.bundle_packer import pack_piuu_bundle, verify_piuu_bundle
from .system.benchmark import run_benchmark
from .system.task_executor import execute_autonomous_task
from .system.object_comparator import ObjectComparator
from .system.monitor import WorkspaceMonitor
from .system.build_doctor import diagnose_android_build

__all__ = [
    "json", "py", "workflow", "system",
    "JSONSuite", "ComplexityAnalyzer", "analyze_workspace", "workspace_summary",
    "batch_code_replace", "inject_import", "scaffold_compose_component", "scaffold_repository",
    "get_system_telemetry", "get_installed_toolchains", "parse_stacktrace",
    "TaskDAG", "AgentMesh", "AgentChannel", "run_agent_loop",
    "probe_agent_environment", "AgentMemoryStore", "compress_log_trace", "pack_agent_context",
    "auto_heal_error", "ensure_path_configured", "ResourceLock",
    "scan_directory", "sanitize_workspace", "fast_search", "inspect_dependencies",
    "get_git_status", "sync_branches", "validate_jni_contracts", "pack_piuu_bundle",
    "verify_piuu_bundle", "run_benchmark", "execute_autonomous_task", "ObjectComparator",
    "WorkspaceMonitor", "diagnose_android_build"
]
