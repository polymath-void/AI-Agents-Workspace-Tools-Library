import unittest
import os
import json
import shutil
from pathlib import Path
from lib.scanner import scan_directory
from lib.manager import sanitize_workspace
from lib.analyzer import ComplexityAnalyzer, analyze_workspace, workspace_summary
from lib.monitor import WorkspaceMonitor
from lib.fast_finder import fast_search
from lib.dep_inspector import inspect_dependencies
from lib.git_helper import get_git_status
from lib.env_checker import get_system_telemetry, get_installed_toolchains
from lib.registry import get_registry_catalog
from lib.code_modder import batch_code_replace, inject_import
from lib.build_doctor import diagnose_android_build
from lib.bundle_packer import pack_piuu_bundle, verify_piuu_bundle
from lib.benchmark import run_benchmark
from lib.task_executor import execute_autonomous_task
from lib.agent_memory import AgentMemoryStore
from lib.contract_validator import validate_jni_contracts
from lib.scaffolder import scaffold_compose_component, scaffold_repository
from lib.crash_doctor import parse_stacktrace
from lib.agent_probe import probe_agent_environment
from lib.error_healer import auto_heal_error, ensure_path_configured
from lib.agent_loop import run_agent_loop
from lib.task_dag import TaskDAG
from lib.agent_channel import AgentChannel
from lib.context_pack import compress_log_trace, pack_agent_context
from lib.resource_lock import ResourceLock
from lib.agent_mesh import AgentMesh
from lib.object_comparator import ObjectComparator
from lib.json_suite import JSONSuite
from wie.storage.memory import WIEMemory

class TestWorkspaceTools(unittest.TestCase):
    def setUp(self):
        self.sandbox = Path(os.environ.get('HOME', '/tmp')) / 'workspace_test_sandbox'
        if self.sandbox.exists():
            shutil.rmtree(self.sandbox)
        self.sandbox.mkdir(parents=True, exist_ok=True)
        (self.sandbox / 'test_file.py').write_text('def test():\n    if True:\n        return 1\n')
        (self.sandbox / 'build').mkdir(exist_ok=True)
        (self.sandbox / 'build' / 'temp.o').write_text('dummy')
        (self.sandbox / 'package.json').write_text('{"name": "test-pkg", "version": "1.0.0", "dependencies": {"express": "^4.18.0"}}')

    def tearDown(self):
        if self.sandbox.exists():
            shutil.rmtree(self.sandbox)

    def test_scanner(self):
        tree = scan_directory(self.sandbox)
        self.assertIsNotNone(tree)
        self.assertEqual(tree['name'], 'workspace_test_sandbox')
        self.assertGreaterEqual(tree['total_files'], 3)
        self.assertGreaterEqual(tree['total_dirs'], 1)

    def test_manager_dry_run(self):
        would_remove = sanitize_workspace(self.sandbox, ['*.o'], dry_run=True)
        self.assertTrue(any('temp.o' in item for item in would_remove))
        self.assertTrue((self.sandbox / 'build' / 'temp.o').exists())

    def test_manager_sanitize(self):
        removed = sanitize_workspace(self.sandbox, ['*.o'])
        self.assertTrue(any('temp.o' in item for item in removed))
        self.assertFalse((self.sandbox / 'build' / 'temp.o').exists())

    def test_analyzer(self):
        analyzer = ComplexityAnalyzer(self.sandbox / 'test_file.py')
        complexity = analyzer.calculate_complexity()
        self.assertEqual(complexity, 2)
        
        metrics = analyzer.calculate_metrics()
        self.assertEqual(metrics['functions'], 1)
        self.assertEqual(metrics['complexity'], 2)

        summary = workspace_summary(self.sandbox)
        self.assertEqual(summary['total_files'], 1)
        self.assertEqual(summary['total_functions'], 1)

    def test_fast_finder(self):
        matches = fast_search(self.sandbox, "return 1", extensions=["py"])
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["line_number"], 3)

    def test_code_modder(self):
        res = batch_code_replace(self.sandbox, "return 1", "return 42", extensions=["py"])
        self.assertEqual(res["total_occurrences"], 1)
        self.assertIn("return 42", (self.sandbox / "test_file.py").read_text())

    def test_dep_inspector(self):
        deps = inspect_dependencies(self.sandbox)
        self.assertEqual(len(deps["npm"]), 1)
        self.assertEqual(deps["npm"][0]["name"], "test-pkg")
        self.assertIn("express", deps["npm"][0]["dependencies"])

    def test_bundle_packer(self):
        ext_dir = self.sandbox / "my_ext"
        ext_dir.mkdir(exist_ok=True)
        (ext_dir / "index.js").write_text("console.log('ext');")
        bundle_out = self.sandbox / "dist" / "my_ext.piuu"
        
        res = pack_piuu_bundle(ext_dir, bundle_out, name="Test Extension")
        self.assertTrue(bundle_out.exists())
        self.assertIsNotNone(res["sha256"])

        verify = verify_piuu_bundle(bundle_out)
        self.assertTrue(verify["valid"])
        self.assertEqual(verify["manifest"]["name"], "Test Extension")

    def test_benchmark(self):
        res = run_benchmark(["python3", "-c", "print(123)"], iterations=2, max_allowed_seconds=2.0)
        self.assertTrue(res["success"])
        self.assertTrue(res["meets_threshold"])

    def test_task_executor(self):
        receipt = execute_autonomous_task("Unit Test Pipeline", target_dir=self.sandbox, run_tests=False)
        self.assertTrue(receipt["success"])
        self.assertIn("environment", receipt["phases"])

    def test_agent_memory(self):
        mem_db = self.sandbox / "test_memory.db"
        store = AgentMemoryStore(mem_db)
        store.set("test_key", {"status": "ok"}, category="test")
        val = store.get("test_key")
        self.assertEqual(val.get("status"), "ok")

    def test_contract_validator(self):
        (self.sandbox / "Native.kt").write_text("class Native { external fun nativeTest(): Int }")
        res = validate_jni_contracts(self.sandbox)
        self.assertEqual(len(res["kotlin_external_functions"]), 1)

    def test_scaffolder(self):
        comp_file = self.sandbox / "TestCard.kt"
        scaffold_compose_component(comp_file)
        self.assertTrue(comp_file.exists())
        self.assertIn("@Composable", comp_file.read_text())

    def test_crash_doctor(self):
        sample_log = "java.lang.NullPointerException: Object was null\n at com.piuu.launcher.MainActivity.onCreate(MainActivity.kt:42)"
        diag = parse_stacktrace(sample_log)
        self.assertEqual(diag["exception_type"], "java.lang.NullPointerException")
        self.assertEqual(diag["root_cause_file"], "MainActivity.kt")
        self.assertEqual(diag["root_cause_line"], 42)

    def test_agent_probe(self):
        report = probe_agent_environment()
        self.assertIn("status", report)
        self.assertIn("checks", report)

    def test_error_healer(self):
        fixes = auto_heal_error("sqlite3.OperationalError: database is locked")
        self.assertIsInstance(fixes, list)

    def test_agent_loop(self):
        res = run_agent_loop(["python3", "-c", "print('hello loop')"], target_dir=str(self.sandbox))
        self.assertTrue(res["success"])
        self.assertEqual(res["status"], "COMPLETED")

    def test_task_dag(self):
        dag = TaskDAG()
        dag.add_task("t1", "Task 1", ["python3", "-c", "print('1')"])
        dag.add_task("t2", "Task 2", ["python3", "-c", "print('2')"], dependencies=["t1"])
        res = dag.run_all(max_workers=2, cwd=str(self.sandbox))
        self.assertEqual(res["completed"], 2)
        self.assertEqual(res["failed"], 0)

    def test_agent_channel(self):
        ch_db = self.sandbox / "test_channel.db"
        channel = AgentChannel(ch_db)
        msg_id = channel.publish("test_topic", {"action": "build"}, sender="Tester")
        self.assertGreater(msg_id, 0)
        msgs = channel.read_topic(topic="test_topic")
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0]["payload"]["action"], "build")

    def test_context_pack(self):
        raw = "\x1b[31mError\x1b[0m\nLine 1\nLine 1\nLine 1\nLine 2"
        comp = compress_log_trace(raw)
        self.assertNotIn("\x1b[31m", comp)
        self.assertIn("repeated 3 times", comp)

    def test_resource_lock(self):
        lock_dir = self.sandbox / "locks"
        locker = ResourceLock(lock_dir)
        acq = locker.acquire("test_resource", holder="AgentA", ttl_seconds=5)
        self.assertTrue(acq)
        st = locker.status("test_resource")
        self.assertTrue(st["locked"])
        rel = locker.release("test_resource", holder="AgentA")
        self.assertTrue(rel)

    def test_agent_mesh(self):
        mesh = AgentMesh()
        mesh.register_subagent("builder_01", "Implementer")
        task = mesh.assign_task("builder_01", "Scaffold Component")
        self.assertEqual(task["role"], "Implementer")
        comp = mesh.complete_task("builder_01", "SUCCESS")
        self.assertEqual(comp["outcome"], "SUCCESS")

    def test_object_comparator(self):
        cmp = ObjectComparator()
        self.assertEqual(cmp.identify_object_type('{"key": "val"}'), "JSON_OBJECT")
        self.assertEqual(cmp.identify_object_type("class MyTest:\n    def run(self): pass"), "PYTHON_CODE_OBJECT")

        diff = cmp.compare_json_objects({"a": 1, "b": 2}, {"a": 1, "b": 99, "c": 3})
        self.assertIn("c", diff["added"])
        self.assertEqual(diff["value_diffs"][0]["key"], "b")

    def test_json_suite(self):
        data = {"users": [{"name": "Alice", "role": "admin"}, {"name": "Bob", "role": "dev"}]}
        self.assertEqual(JSONSuite.query(data, "users[0].name"), "Alice")

        JSONSuite.patch_set(data, "users[1].active", True)
        self.assertTrue(JSONSuite.query(data, "users[1].active"))

        schema = {"required": ["name"], "types": {"name": "str"}}
        valid = JSONSuite.validate_schema({"name": "Alice"}, schema)
        self.assertTrue(valid["valid"])

    def test_env_checker(self):
        telem = get_system_telemetry()
        self.assertIn("python_version", telem)
        self.assertGreater(telem["total_ram_mb"], 0)
        tools = get_installed_toolchains()
        self.assertIn("python3", tools)

    def test_registry(self):
        catalog = get_registry_catalog()
        self.assertGreaterEqual(len(catalog), 27)

    def test_monitor(self):
        monitor = WorkspaceMonitor()
        anomalies = monitor.check_health(self.sandbox)
        self.assertIsInstance(anomalies, list)

    def test_memory_db(self):
        db_file = self.sandbox / 'storage' / 'wie_test.db'
        memory = WIEMemory(db_file)
        memory.log_event("CREATED", str(self.sandbox / 'test_file.py'))
        recent = memory.get_recent_events(limit=5)
        self.assertGreaterEqual(len(recent), 1)

if __name__ == '__main__':
    unittest.main()
