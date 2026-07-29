"""Tests for scripts/build_spec.py rendering, run with pytest.

Fixture shapes mirror the real field-definitions.json artifacts (schemas v26.0803):
`values` is a list of {"value": str, "description"?: str} and always co-occurs with
`values_exhaustive`; values-carrying fields may be type "enum" OR "string"; two trial
fields are type "enum" with no `values` key at all.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_spec  # noqa: E402


def _closed_field(**over):
    f = {
        "name": "status", "type": "string", "requirement": "required",
        "description": "Lifecycle state of the run.",
        "values": [
            {"value": "complete", "description": "The run reached its final activity."},
            {"value": "abandoned", "description": "The run stopped before its final activity."},
        ],
        "values_exhaustive": True,
    }
    f.update(over)
    return f


def _open_field(**over):
    f = {
        "name": "stimulus_role", "type": "enum", "requirement": "optional",
        "description": "The role the stimulus plays within the trial.",
        "values": [
            {"value": "target", "description": "A stimulus the agent must process."},
            {"value": "non_target", "description": "Processed but not response-triggering."},
        ],
        "values_exhaustive": False,
    }
    f.update(over)
    return f


# --- inline rendering (field table cell) ----------------------------------------------------

def test_values_names_render_inline_in_field_cell():
    row = build_spec._field_rows([_closed_field()])[-1]
    assert "*Values:* `complete` · `abandoned`" in row


def test_open_value_set_renders_inline_as_known_values():
    row = build_spec._field_rows([_open_field()])[-1]
    assert "*Known values:* `target` · `non_target`" in row
    assert "*Values:*" not in row


def test_enum_typed_field_without_values_renders_as_before():
    f = {"name": "adaptive_method_name", "type": "enum", "requirement": "optional",
         "description": "Name of the adaptive procedure."}
    row = build_spec._field_rows([f])[-1]
    assert "Values" not in row
    assert row.startswith("| `adaptive_method_name` | enum |")


def test_long_value_list_defers_names_to_the_definitions_section():
    values = [{"value": f"task_variant_{i:02d}", "description": "One task."} for i in range(22)]
    row = build_spec._field_rows([_closed_field(values=values)])[-1]
    assert "task_variant_03" not in row          # not inlined
    assert "*Values:* 22, defined below." in row


# --- the full-width value-definitions section -----------------------------------------------

def test_value_definitions_section_lists_values_with_descriptions():
    lines = build_spec._value_definition_sections([_closed_field()])
    text = "\n".join(lines)
    assert "## Value definitions" in text
    assert "### `status`" in text
    assert "| `complete` | The run reached its final activity. |" in text


def test_open_set_section_states_the_set_is_open():
    text = "\n".join(build_spec._value_definition_sections([_open_field()]))
    assert "The set is open: datasets may contain values not listed here." in text


def test_closed_set_section_has_no_openness_sentence():
    text = "\n".join(build_spec._value_definition_sections([_closed_field()]))
    assert "set is open" not in text


def test_fully_descriptionless_values_get_no_section():
    f = _closed_field(values=[{"value": "a"}, {"value": "b"}])
    assert build_spec._value_definition_sections([f]) == []


def test_descriptionless_but_deferred_long_list_is_still_sectioned():
    values = [{"value": f"v{i:02d}"} for i in range(40)]
    text = "\n".join(build_spec._value_definition_sections([_closed_field(values=values)]))
    assert "### `status`" in text and "| `v39` |" in text


def test_value_with_missing_description_gets_empty_cell():
    f = _closed_field(values=[{"value": "a", "description": "Documented."}, {"value": "b"}])
    text = "\n".join(build_spec._value_definition_sections([f]))
    assert "| `b` |  |" in text


# --- page integration -----------------------------------------------------------------------

def test_table_page_appends_value_definitions_after_field_tables():
    table = {"name": "Response", "fields": [_open_field()]}
    page = build_spec.render_table_page("trial", table, "https://x/trial")
    assert page.index("## Value definitions") > page.index("| `stimulus_role` |")


def test_flat_page_appends_value_definitions(tmp_path, monkeypatch):
    monkeypatch.setattr(build_spec, "SPEC_DIR", tmp_path)
    doc = {"version": "26.0803", "fields": [_closed_field()]}
    build_spec.generate_schema_pages("dataset", doc, "https://x")
    page = (tmp_path / "dataset" / "index.qmd").read_text()
    assert "## Value definitions" in page and "### `status`" in page


# --- glossary -------------------------------------------------------------------------------

def test_glossary_entry_carries_value_names():
    doc = {"tables": [{"name": "StudyflowLog", "fields": [_closed_field()]}]}
    (entry,) = build_spec._schema_term_entries("studyflow", doc, skip=set())
    assert "Values: `complete`, `abandoned`." in " ".join(entry.get("notes", []))


def test_glossary_entry_marks_open_sets_as_known_values():
    doc = {"tables": [{"name": "Response", "fields": [_open_field()]}]}
    (entry,) = build_spec._schema_term_entries("trial", doc, skip=set())
    assert "Known values: `target`, `non_target`." in " ".join(entry.get("notes", []))
