from typing import Dict, Iterable, List

from .estimator import CostBreakdown


def _format_currency(value: float, currency: str) -> str:
    return f"{currency} {value:,.2f}"


def generate_markdown_table(results: Dict[str, CostBreakdown]) -> str:
    """Generate a Markdown table comparing monthly costs across models."""
    # Sort by total cost ascending
    rows: List[CostBreakdown] = sorted(
        results.values(), key=lambda r: r.total_cost
    )

    if not rows:
        return "No results."

    header = [
        "Provider",
        "Model",
        "Prompt tokens/call",
        "Completion tokens/call",
        "Calls/month",
        "Total prompt tokens",
        "Total completion tokens",
        "Input cost",
        "Output cost",
        "Total cost",
    ]

    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
    ]

    for r in rows:
        currency = r.currency
        line = [
            r.provider,
            r.display_name,
            f"{r.prompt_tokens_per_call:,}",
            f"{r.completion_tokens_per_call:,}",
            f"{r.calls_per_month:,}",
            f"{r.total_prompt_tokens:,}",
            f"{r.total_completion_tokens:,}",
            _format_currency(r.input_cost, currency),
            _format_currency(r.output_cost, currency),
            _format_currency(r.total_cost, currency),
        ]
        lines.append("| " + " | ".join(line) + " |")

    return "\n".join(lines)


