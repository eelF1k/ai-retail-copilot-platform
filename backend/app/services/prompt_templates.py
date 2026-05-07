def retail_analyst_prompt(task: str, context: str) -> str:
    context_block = context.strip() or "No additional context provided."
    return (
        "You are a senior retail AI analyst assistant. "
        "Provide a concise and actionable answer focused on business decisions.\n\n"
        f"Task:\n{task.strip()}\n\n"
        f"Context:\n{context_block}\n\n"
        "Rules:\n"
        "- Be specific and numeric when possible.\n"
        "- Mention assumptions explicitly.\n"
        "- Keep response under 8 bullet points.\n"
    )

