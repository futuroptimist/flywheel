from scripts.update_prompt_docs_summary import markdown_table


def test_markdown_table_no_wrap():
    long_link = "[link](https://example.com/" + "a" * 150 + ")"
    table = markdown_table([[long_link, "evergreen"]], ["Prompt", "Type"])
    lines = table.splitlines()
    assert lines[0] == "| Prompt | Type |"
    assert lines[1] == "| --- | --- |"
    assert lines[2].startswith("| [link](https://example.com/")
    assert len(lines[2].splitlines()) == 1
