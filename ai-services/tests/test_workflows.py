import pytest
from workflows.step import WorkflowStep
from workflows.state import WorkflowState
from workflows.registry import WorkflowRegistry, workflow_registry
from workflows.engine import WorkflowEngine

# Import builtins to trigger registration
import workflows.builtin.investigation
import workflows.builtin.case_analysis
import workflows.builtin.suspect_profile
import workflows.builtin.crime_briefing


class TestWorkflowStep:
    def test_create_step(self):
        async def dummy(state):
            return "done"
        step = WorkflowStep(name="test", func=dummy, description="Test step")
        assert step.name == "test"
        assert step.status == "pending"

    def test_to_dict(self):
        async def dummy(state):
            return "done"
        step = WorkflowStep(name="test", func=dummy, depends_on=["step1"])
        d = step.to_dict()
        assert d["name"] == "test"
        assert "step1" in d["depends_on"]


class TestWorkflowState:
    def test_set_get(self):
        state = WorkflowState()
        state.set("key", "value")
        assert state.get("key") == "value"

    def test_get_default(self):
        state = WorkflowState()
        assert state.get("missing", "default") == "default"

    def test_step_result(self):
        state = WorkflowState()
        state.set_step_result("step1", {"result": "ok"})
        assert state.get_step_result("step1")["result"] == "ok"
        assert state.get("step_step1")["result"] == "ok"

    def test_clear(self):
        state = WorkflowState({"a": 1})
        state.clear()
        assert state.get_all() == {}

    def test_initial_state(self):
        state = WorkflowState({"x": 10})
        assert state.get("x") == 10


class TestWorkflowRegistry:
    def test_register_and_get(self):
        reg = WorkflowRegistry()
        reg.register("test_wf", {"description": "Test", "steps": [{"name": "s1"}]})
        wf = reg.get("test_wf")
        assert wf["description"] == "Test"

    def test_list_all(self):
        reg = WorkflowRegistry()
        reg.register("wf1", {"description": "WF1", "steps": [{"name": "a"}, {"name": "b"}]})
        reg.register("wf2", {"description": "WF2", "steps": [{"name": "c"}]})
        all_wfs = reg.list_all()
        assert len(all_wfs) == 2

    def test_get_missing(self):
        reg = WorkflowRegistry()
        assert reg.get("nonexistent") is None

    def test_step_names(self):
        reg = WorkflowRegistry()
        reg.register("wf", {"steps": [{"name": "s1"}, {"name": "s2"}]})
        names = reg.get_step_names("wf")
        assert names == ["s1", "s2"]


class TestWorkflowEngine:
    def setup_method(self):
        self.engine = WorkflowEngine()

    @pytest.mark.asyncio
    async def test_run_simple_workflow(self):
        async def step_a(state):
            return {"result": "a_done"}

        async def step_b(state):
            a_result = state.get_step_result("a")
            return {"result": "b_done", "a_says": a_result.get("result")}

        reg = WorkflowRegistry()
        reg.register("simple", {
            "description": "Simple test",
            "steps": [
                {"name": "a", "func": step_a, "description": "Step A"},
                {"name": "b", "func": step_b, "description": "Step B", "depends_on": ["a"]},
            ],
        })

        engine = WorkflowEngine()
        engine.registry = reg
        result = await engine.run("simple")
        assert result["status"] == "completed"
        assert result["completed"] == 2

    @pytest.mark.asyncio
    async def test_run_missing_workflow(self):
        result = await self.engine.run("nonexistent")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_workflow_with_state(self):
        async def read_input(state):
            return {"query": state.get("query", "")}

        reg = WorkflowRegistry()
        reg.register("with_input", {
            "description": "Uses input",
            "steps": [{"name": "read", "func": read_input}],
        })

        engine = WorkflowEngine()
        engine.registry = reg
        result = await engine.run("with_input", {"query": "theft cases"})
        assert result["result"]["step_read"]["query"] == "theft cases"

    def test_list_workflows(self):
        wfs = self.engine.list_workflows()
        assert isinstance(wfs, list)

    def test_get_workflow(self):
        wf = self.engine.get_workflow("investigation")
        assert wf is not None
        assert wf["name"] == "investigation"


class TestBuiltinWorkflows:
    def test_investigation_registered(self):
        assert workflow_registry.get("investigation") is not None

    def test_case_analysis_registered(self):
        assert workflow_registry.get("case_analysis") is not None

    def test_suspect_profile_registered(self):
        assert workflow_registry.get("suspect_profile") is not None

    def test_crime_briefing_registered(self):
        assert workflow_registry.get("crime_briefing") is not None

    def test_all_workflows_listed(self):
        all_wfs = workflow_registry.list_all()
        names = [w["name"] for w in all_wfs]
        assert "investigation" in names
        assert "case_analysis" in names
        assert "suspect_profile" in names
        assert "crime_briefing" in names

    @pytest.mark.asyncio
    async def test_run_crime_briefing(self):
        engine = WorkflowEngine()
        result = await engine.run("crime_briefing")
        assert result["status"] == "completed"
        assert result["completed"] == 5
