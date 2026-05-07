from app.services.prompt_templates import retail_analyst_prompt


def test_retail_analyst_prompt_contains_task_and_context():
    prompt = retail_analyst_prompt(
        task="Find weak categories in last 30 days",
        context="Store: VELMART_KYIV; focus on margin drop",
    )

    assert "Find weak categories" in prompt
    assert "VELMART_KYIV" in prompt
    assert "Rules:" in prompt

