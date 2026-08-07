import unittest
import os
import json
import shutil
from pathlib import Path

# Test direct modular imports
from lib.json import (
    JSONSuite, PromptJSONProcessor, JSONFormatter,
    JSONSchemaGenerator, JSONFlattener, NDJSONSuite,
    JSONCSVBridge, JSONStatsInspector, JSONFilterEngine,
    JSONSanitizer
)
from lib.py import (
    ComplexityAnalyzer, analyze_workspace, workspace_summary,
    batch_code_replace, inject_import,
    scaffold_compose_component, scaffold_repository,
    get_system_telemetry, get_installed_toolchains,
    parse_stacktrace
)
from lib.workflow import (
    TaskDAG, AgentMesh, AgentChannel, run_agent_loop,
    probe_agent_environment, AgentMemoryStore,
    compress_log_trace, pack_agent_context,
    auto_heal_error, ensure_path_configured, ResourceLock,
    WorkflowContextManager, SwarmDispatcher
)
from lib.system import (
    scan_directory, sanitize_workspace, fast_search,
    inspect_dependencies, get_git_status, sync_branches,
    validate_jni_contracts, pack_piuu_bundle, verify_piuu_bundle,
    run_benchmark, execute_autonomous_task, ObjectComparator,
    WorkspaceMonitor, diagnose_android_build
)
from lib.registry import get_registry_catalog
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

    def test_json_suite_modular(self):
        data = {"users": [{"name": "Alice", "role": "admin"}, {"name": "Bob", "role": "dev"}]}
        self.assertEqual(JSONSuite.query(data, "users[0].name"), "Alice")

        JSONSuite.patch_set(data, "users[1].active", True)
        self.assertTrue(JSONSuite.query(data, "users[1].active"))

        schema = {"required": ["name"], "types": {"name": "str"}}
        valid = JSONSuite.validate_schema({"name": "Alice"}, schema)
        self.assertTrue(valid["valid"])

    def test_json_extended_suite(self):
        # 1. Formatter
        formatted = JSONFormatter.format({"b": 2, "a": 1}, sort_keys=True, minify=True)
        self.assertEqual(formatted, '{"a":1,"b":2}')

        # 2. Schema Gen
        schema = JSONSchemaGenerator.infer_schema({"name": "Piuu", "count": 10})
        self.assertEqual(schema["type"], "object")
        self.assertIn("count", schema["properties"])

        # 3. Flattener & Unflattener
        nested = {"user": {"profile": {"name": "Alice"}}}
        flat = JSONFlattener.flatten(nested)
        self.assertEqual(flat.get("user.profile.name"), "Alice")
        unflat = JSONFlattener.unflatten(flat)
        self.assertEqual(unflat["user"]["profile"]["name"], "Alice")

        # 4. NDJSON
        items = [{"id": 1}, {"id": 2}]
        nd = NDJSONSuite.json_to_ndjson(items)
        self.assertEqual(len(nd.split("\n")), 2)
        parsed = NDJSONSuite.ndjson_to_json(nd)
        self.assertEqual(len(parsed), 2)

        # 5. CSV Bridge
        csv_str = JSONCSVBridge.json_to_csv([{"id": 1, "name": "App"}])
        self.assertIn("id,name", csv_str)
        back_json = JSONCSVBridge.csv_to_json(csv_str)
        self.assertEqual(back_json[0]["id"], 1)

        # 6. Stats Inspector
        stats = JSONStatsInspector.inspect(nested)
        self.assertEqual(stats["max_depth"], 4)
        self.assertEqual(stats["total_keys"], 3)

        # 7. Filter Engine
        collection = [{"name": "A", "age": 20}, {"name": "B", "age": 35}]
        filtered = JSONFilterEngine.filter_array(collection, "age", ">", 30)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["name"], "B")

        # 8. Sanitizer
        secret_obj = {"apiKey": "12345-secret", "email": "user@example.com", "public": "ok"}
        sanitized = JSONSanitizer.sanitize(secret_obj)
        self.assertEqual(sanitized["apiKey"], "***REDACTED***")
        self.assertEqual(sanitized["email"], "***REDACTED***")
        self.assertEqual(sanitized["public"], "ok")

    def test_prompt_json_processor(self):
        messy_prompt = "Hey please configure the build: {targetSdk: 35, 'version': '2.0', active: True,}"
        extracted = PromptJSONProcessor.extract_json_from_prompt(messy_prompt)
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted["targetSdk"], 35)
        self.assertEqual(extracted["version"], "2.0")
        self.assertTrue(extracted["active"])

        intent = PromptJSONProcessor.normalize_prompt_intent("Please fix build and update app/build.gradle")
        self.assertEqual(intent["detected_action"], "BUILD_REPAIR")
        self.assertIn("app/build.gradle", intent["parameters"]["referenced_files"])

    def test_workflow_context_manager(self):
        ctx_db = self.sandbox / "wf_context.db"
        mgr = WorkflowContextManager(ctx_db)
        mgr.register_workflow("wf_build", "Build Subagent")
        mgr.set_frame("wf_build", "targetSdk", 35)
        mgr.set_frame("wf_build", "compose_version", "1.7.0")

        ctx = mgr.get_context("wf_build")
        self.assertEqual(ctx["frames"]["targetSdk"]["value"], 35)

        mgr.register_workflow("wf_verify", "Verification Subagent")
        hnd = mgr.handoff_context("wf_build", "wf_verify", keys=["targetSdk"])
        self.assertIn("targetSdk", hnd["transferred_keys"])

        verify_ctx = mgr.get_context("wf_verify")
        self.assertEqual(verify_ctx["frames"]["targetSdk"]["value"], 35)
        self.assertNotIn("compose_version", verify_ctx["frames"])

    def test_swarm_dispatcher(self):
        eval_res = SwarmDispatcher.evaluate_subagent_need("Perform broad research across codebase", is_exploratory=True)
        self.assertTrue(eval_res["should_launch_subagent"])
        self.assertEqual(eval_res["suggested_type"], "research")

        spec = SwarmDispatcher.build_dispatch_spec("BuildDoctor", "Fix 16KB memory page alignment in C headers")
        self.assertEqual(spec["Role"], "BuildDoctor")
        self.assertIn("16KB", spec["Prompt"])

        agg = SwarmDispatcher.aggregate_subagent_outcomes([
            {"subagent": "builder", "status": "SUCCESS"},
            {"subagent": "verifier", "status": "PASSED"}
        ])
        self.assertTrue(agg["consensus_passed"])
        self.assertEqual(agg["succeeded"], 2)

    def test_python_suite_modular(self):
        analyzer = ComplexityAnalyzer(self.sandbox / 'test_file.py')
        self.assertEqual(analyzer.calculate_complexity(), 2)

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

    def test_env_checker(self):
        telem = get_system_telemetry()
        self.assertIn("python_version", telem)
        self.assertGreater(telem["total_ram_mb"], 0)
        tools = get_installed_toolchains()
        self.assertIn("python3", tools)

    def test_registry(self):
        catalog = get_registry_catalog()
        self.assertGreaterEqual(len(catalog), 33)

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
