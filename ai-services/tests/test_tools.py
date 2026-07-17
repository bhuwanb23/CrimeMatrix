import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from tools.http_tool import BackendTool
from tools.crime.search import CrimeSearchTool
from tools.crime.detail import CrimeDetailTool
from tools.crime.list import CrimeListTool
from tools.crime.stats import CrimeStatsTool
from tools.graph.traverse import GraphTraverseTool
from tools.graph.shortest import GraphShortestPathTool
from tools.graph.neighbors import GraphNeighborsTool
from tools.analytics.counts import AnalyticsCountsTool
from tools.analytics.trends import AnalyticsTrendsTool
from tools.investigation.notes import InvestigationNotesTool
from tools.investigation.timeline import InvestigationTimelineTool
from tools.investigation.status import CaseStatusTool
from tools.report.generate import ReportGenerateTool
from tools.rag.search import RAGSearchTool


class TestBackendTool:
    def test_schema(self):
        tool = CrimeSearchTool()
        schema = tool.to_schema()
        assert schema["name"] == "crime_search"
        assert "description" in schema
        assert "parameters" in schema

    @pytest.mark.asyncio
    async def test_get_error_handling(self):
        tool = CrimeSearchTool(base_url="http://localhost:99999")
        result = await tool._get("/nonexistent")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_post_error_handling(self):
        tool = CrimeSearchTool(base_url="http://localhost:99999")
        result = await tool._post("/nonexistent", {})
        assert "error" in result


class TestCrimeTools:
    def test_search_schema(self):
        tool = CrimeSearchTool()
        assert tool.get_name() == "crime_search"
        assert "query" in tool.get_parameters()["properties"]

    def test_detail_schema(self):
        tool = CrimeDetailTool()
        assert tool.get_name() == "crime_detail"
        assert "crime_id" in tool.get_parameters()["required"]

    def test_list_schema(self):
        tool = CrimeListTool()
        assert tool.get_name() == "crime_list"

    def test_stats_schema(self):
        tool = CrimeStatsTool()
        assert tool.get_name() == "crime_stats"


class TestGraphTools:
    def test_traverse_schema(self):
        tool = GraphTraverseTool()
        assert tool.get_name() == "graph_traverse"
        assert "node_id" in tool.get_parameters()["required"]

    def test_shortest_schema(self):
        tool = GraphShortestPathTool()
        assert tool.get_name() == "graph_shortest"
        assert "source" in tool.get_parameters()["required"]
        assert "target" in tool.get_parameters()["required"]

    def test_neighbors_schema(self):
        tool = GraphNeighborsTool()
        assert tool.get_name() == "graph_neighbors"
        assert "node_id" in tool.get_parameters()["required"]


class TestAnalyticsTools:
    def test_counts_schema(self):
        tool = AnalyticsCountsTool()
        assert tool.get_name() == "analytics_counts"

    def test_trends_schema(self):
        tool = AnalyticsTrendsTool()
        assert tool.get_name() == "analytics_trends"


class TestInvestigationTools:
    def test_notes_schema(self):
        tool = InvestigationNotesTool()
        assert tool.get_name() == "investigation_notes"

    def test_timeline_schema(self):
        tool = InvestigationTimelineTool()
        assert tool.get_name() == "investigation_timeline"
        assert "investigation_id" in tool.get_parameters()["required"]

    def test_status_schema(self):
        tool = CaseStatusTool()
        assert tool.get_name() == "case_status"
        assert "new_status" in tool.get_parameters()["required"]


class TestReportTool:
    def test_generate_schema(self):
        tool = ReportGenerateTool()
        assert tool.get_name() == "report_generate"
        assert "crime_id" in tool.get_parameters()["required"]


class TestRAGTool:
    def test_search_schema(self):
        tool = RAGSearchTool()
        assert tool.get_name() == "rag_search"
        assert "query" in tool.get_parameters()["required"]


class TestToolRegistry:
    def test_register_and_list(self):
        from tools.registry import ToolRegistry
        reg = ToolRegistry()
        reg.register(CrimeSearchTool())
        reg.register(CalculatorTool())
        names = reg.list_names()
        assert "crime_search" in names
        assert "calculator" in names

    def test_get(self):
        from tools.registry import ToolRegistry
        reg = ToolRegistry()
        reg.register(CrimeSearchTool())
        tool = reg.get("crime_search")
        assert tool is not None
        assert tool.get_name() == "crime_search"

    def test_get_missing(self):
        from tools.registry import ToolRegistry
        reg = ToolRegistry()
        assert reg.get("nonexistent") is None

    @pytest.mark.asyncio
    async def test_invoke_missing(self):
        from tools.registry import ToolRegistry
        reg = ToolRegistry()
        with pytest.raises(ValueError):
            await reg.invoke("nonexistent")


from tools.builtins.calculator import CalculatorTool


class TestCalculatorTool:
    def test_schema(self):
        tool = CalculatorTool()
        assert tool.get_name() == "calculator"

    @pytest.mark.asyncio
    async def test_execute(self):
        tool = CalculatorTool()
        result = await tool.execute(expression="2 + 3")
        data = json.loads(result)
        assert data["result"] == 5

    @pytest.mark.asyncio
    async def test_invalid_expression(self):
        tool = CalculatorTool()
        result = await tool.execute(expression="import os")
        data = json.loads(result)
        assert "error" in data
