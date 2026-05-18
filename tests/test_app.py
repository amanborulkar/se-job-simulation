"""
test_app.py
===========
Automated test suite for the SWE Job Simulator Dash application.

Tests are written using both unittest.TestCase (for CI compatibility) and
bare pytest functions, so they run under either test runner.

Run with:
    pytest tests/test_app.py -v

CI trigger:
    pytest tests/test_app.py -v --tb=short --junitxml=reports/junit.xml
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, JOB_DATA, REGIONS, make_openings_bar, make_salary_scatter, make_remote_gauge, make_role_radar



class TestLayoutStructure(unittest.TestCase):
    """Verify top-level layout components exist in the Dash app."""

    def setUp(self):
        self.layout = app.layout

    def test_header_is_present(self):
        """The layout must contain an element with id='app-header'."""
        header = self._find_component_by_id(self.layout, "app-header")
        self.assertIsNotNone(header, "app-header component not found in layout")

    def test_header_title_text(self):
        """The header title component must carry the app name."""
        title = self._find_component_by_id(self.layout, "header-title")
        self.assertIsNotNone(title, "header-title not found")
        self.assertEqual(title.children, "SWE Job Simulator")

    def test_region_picker_is_present(self):
        """A Dropdown with id='region-picker' must exist in the layout."""
        from dash import dcc
        picker = self._find_component_by_id(self.layout, "region-picker")
        self.assertIsNotNone(picker, "region-picker component not found in layout")
        self.assertIsInstance(picker, dcc.Dropdown)

    def test_region_picker_default_value(self):
        """Region picker default must be 'Global'."""
        picker = self._find_component_by_id(self.layout, "region-picker")
        self.assertEqual(picker.value, "Global")

    def test_region_picker_has_all_regions(self):
        """Dropdown options must include every region defined in REGIONS."""
        picker = self._find_component_by_id(self.layout, "region-picker")
        option_values = [opt["value"] for opt in picker.options]
        for region in REGIONS:
            self.assertIn(region, option_values, f"Region '{region}' missing from picker options")


    def test_visualisation_section_is_present(self):
        """An element with id='viz-section' must exist."""
        viz = self._find_component_by_id(self.layout, "viz-section")
        self.assertIsNotNone(viz, "viz-section not found in layout")

    def test_openings_bar_graph_present(self):
        """Graph with id='openings-bar' must be in the layout."""
        from dash import dcc
        graph = self._find_component_by_id(self.layout, "openings-bar")
        self.assertIsNotNone(graph, "openings-bar Graph not found")
        self.assertIsInstance(graph, dcc.Graph)

    def test_salary_scatter_graph_present(self):
        """Graph with id='salary-scatter' must be in the layout."""
        from dash import dcc
        graph = self._find_component_by_id(self.layout, "salary-scatter")
        self.assertIsNotNone(graph, "salary-scatter Graph not found")
        self.assertIsInstance(graph, dcc.Graph)

    def test_remote_gauge_graph_present(self):
        """Graph with id='remote-gauge' must be in the layout."""
        from dash import dcc
        graph = self._find_component_by_id(self.layout, "remote-gauge")
        self.assertIsNotNone(graph, "remote-gauge Graph not found")
        self.assertIsInstance(graph, dcc.Graph)

    def test_role_radar_graph_present(self):
        """Graph with id='role-radar' must be in the layout."""
        from dash import dcc
        graph = self._find_component_by_id(self.layout, "role-radar")
        self.assertIsNotNone(graph, "role-radar Graph not found")
        self.assertIsInstance(graph, dcc.Graph)


    def test_kpi_row_present(self):
        """A div with id='kpi-row' must be in the layout."""
        kpi = self._find_component_by_id(self.layout, "kpi-row")
        self.assertIsNotNone(kpi, "kpi-row not found in layout")


    def _find_component_by_id(self, component, target_id):
        """Depth-first search through a Dash component tree by component id."""
        if hasattr(component, "id") and component.id == target_id:
            return component
        children = getattr(component, "children", None)
        if children is None:
            return None
        if not isinstance(children, (list, tuple)):
            children = [children]
        for child in children:
            if hasattr(child, "id") or hasattr(child, "children"):
                result = self._find_component_by_id(child, target_id)
                if result is not None:
                    return result
        return None



class TestJobData(unittest.TestCase):
    """Verify the job data dictionary is well-formed for every region."""

    REQUIRED_KEYS = {"roles", "openings", "avg_salary", "growth", "remote_pct"}

    def test_all_regions_present_in_data(self):
        for region in REGIONS:
            self.assertIn(region, JOB_DATA, f"Region '{region}' missing from JOB_DATA")

    def test_all_required_keys_exist(self):
        for region, data in JOB_DATA.items():
            for key in self.REQUIRED_KEYS:
                self.assertIn(key, data, f"Key '{key}' missing for region '{region}'")

    def test_list_lengths_consistent_per_region(self):
        for region, data in JOB_DATA.items():
            n_roles = len(data["roles"])
            for key in self.REQUIRED_KEYS - {"roles"}:
                self.assertEqual(
                    len(data[key]), n_roles,
                    f"Length mismatch: '{key}' in '{region}' has {len(data[key])} items, expected {n_roles}",
                )

    def test_salary_values_positive(self):
        for region, data in JOB_DATA.items():
            for sal in data["avg_salary"]:
                self.assertGreater(sal, 0, f"Non-positive salary in '{region}'")

    def test_openings_values_positive(self):
        for region, data in JOB_DATA.items():
            for val in data["openings"]:
                self.assertGreater(val, 0, f"Non-positive opening count in '{region}'")

    def test_growth_values_are_percentages(self):
        for region, data in JOB_DATA.items():
            for g in data["growth"]:
                self.assertGreaterEqual(g, 0)
                self.assertLessEqual(g, 100, f"Growth % out of range in '{region}'")

    def test_remote_pct_in_range(self):
        for region, data in JOB_DATA.items():
            for pct in data["remote_pct"]:
                self.assertGreaterEqual(pct, 0)
                self.assertLessEqual(pct, 100, f"remote_pct out of range in '{region}'")


class TestFigures(unittest.TestCase):
    """Verify that figure-builder functions return valid Plotly Figure objects."""

    def _assert_valid_figure(self, fig, name="figure"):
        import plotly.graph_objects as go
        self.assertIsInstance(fig, go.Figure, f"{name} is not a go.Figure")
        self.assertGreater(len(fig.data), 0, f"{name} has no traces")

    def test_openings_bar_returns_figure(self):
        for region in REGIONS:
            fig = make_openings_bar(region)
            self._assert_valid_figure(fig, f"openings_bar[{region}]")

    def test_salary_scatter_returns_figure(self):
        for region in REGIONS:
            fig = make_salary_scatter(region)
            self._assert_valid_figure(fig, f"salary_scatter[{region}]")

    def test_remote_gauge_returns_figure(self):
        for region in REGIONS:
            fig = make_remote_gauge(region)
            self._assert_valid_figure(fig, f"remote_gauge[{region}]")

    def test_role_radar_returns_figure(self):
        for region in REGIONS:
            fig = make_role_radar(region)
            self._assert_valid_figure(fig, f"role_radar[{region}]")

    def test_openings_bar_trace_count(self):
        """Bar chart should have exactly one Bar trace."""
        import plotly.graph_objects as go
        fig = make_openings_bar("Global")
        bar_traces = [t for t in fig.data if isinstance(t, go.Bar)]
        self.assertEqual(len(bar_traces), 1)

    def test_salary_scatter_trace_count(self):
        """Scatter chart should have one trace per role in Global (7)."""
        fig = make_salary_scatter("Global")
        self.assertEqual(len(fig.data), len(JOB_DATA["Global"]["roles"]))

    def test_radar_has_two_traces(self):
        """Radar chart must have two overlaid traces (salary + openings)."""
        fig = make_role_radar("Global")
        self.assertEqual(len(fig.data), 2)

    def test_figures_have_dark_background(self):
        """All figures must use the dark card background colour."""
        expected = "#161E30"
        for fn, label in [
            (make_openings_bar, "openings_bar"),
            (make_salary_scatter, "salary_scatter"),
            (make_remote_gauge, "remote_gauge"),
            (make_role_radar, "role_radar"),
        ]:
            fig = fn("Global")
            self.assertEqual(
                fig.layout.paper_bgcolor.lower(), expected.lower(),
                f"{label} paper_bgcolor is not the expected dark card colour",
            )



class TestAppServer(unittest.TestCase):
    """Verify the Dash/Flask server can be instantiated and pinged."""

    def test_server_attribute_exists(self):
        """app.server must be a Flask instance (for production deploy)."""
        from flask import Flask
        self.assertIsInstance(app.server, Flask)

    def test_app_title(self):
        """Application window title must be set correctly."""
        self.assertEqual(app.title, "SWE Job Simulator")

    def test_flask_test_client_200(self):
        """GET / must return HTTP 200 from the Flask test client."""
        client = app.server.test_client()
        resp = client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_flask_test_client_returns_html(self):
        """Response content-type must be text/html."""
        client = app.server.test_client()
        resp = client.get("/")
        self.assertIn("text/html", resp.content_type)

    def test_layout_assets_loaded(self):
        """The app layout must be a non-None component tree."""
        self.assertIsNotNone(app.layout)


class TestCallbacks(unittest.TestCase):
    """Light integration tests: invoke callback functions directly."""

    def _run_update_dashboard(self, region):
        """Directly call the registered callback logic by importing it."""
        import plotly.graph_objects as go
        from app import update_dashboard
        result = update_dashboard(region)
        return result

    def test_callback_returns_5_outputs(self):
        """update_dashboard callback must return exactly 5 outputs."""
        result = self._run_update_dashboard("Global")
        self.assertEqual(len(result), 5, "Callback must return (kpis, bar, scatter, gauge, radar)")

    def test_callback_all_regions_succeed(self):
        """Callback must not raise for any region in REGIONS."""
        for region in REGIONS:
            try:
                self._run_update_dashboard(region)
            except Exception as e:
                self.fail(f"update_dashboard('{region}') raised {type(e).__name__}: {e}")

    def test_callback_figures_are_go_figure(self):
        """The four figure outputs must be go.Figure instances."""
        import plotly.graph_objects as go
        kpis, bar, scatter, gauge, radar = self._run_update_dashboard("North America")
        for fig, name in [(bar, "bar"), (scatter, "scatter"), (gauge, "gauge"), (radar, "radar")]:
            self.assertIsInstance(fig, go.Figure, f"Output '{name}' is not a go.Figure")

    def test_callback_kpis_are_list(self):
        """KPI output must be a list of Dash components (one per KPI card)."""
        kpis, *_ = self._run_update_dashboard("Europe")
        self.assertIsInstance(kpis, list)
        self.assertEqual(len(kpis), 4, "Expected 4 KPI cards")

def test_regions_list_not_empty():
    assert len(REGIONS) > 0, "REGIONS list must not be empty"


def test_regions_list_contains_global():
    assert "Global" in REGIONS


def test_job_data_keys_match_regions():
    for r in REGIONS:
        assert r in JOB_DATA, f"JOB_DATA missing key for region '{r}'"


def test_make_openings_bar_global():
    fig = make_openings_bar("Global")
    assert fig is not None


def test_make_salary_scatter_india():
    fig = make_salary_scatter("India")
    assert len(fig.data) == len(JOB_DATA["India"]["roles"])


def test_app_layout_not_none():
    assert app.layout is not None


def test_header_id_in_layout():
    """Check that app-header id exists somewhere in layout repr."""
    import json
    layout_repr = str(app.layout)
    assert "app-header" in layout_repr


def test_region_picker_id_in_layout():
    layout_repr = str(app.layout)
    assert "region-picker" in layout_repr


def test_viz_section_id_in_layout():
    layout_repr = str(app.layout)
    assert "viz-section" in layout_repr


if __name__ == "__main__":
    unittest.main(verbosity=2)
