from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ModelPricing:
    """Pricing for a single LLM model.

    Prices are in currency per 1K tokens (or other unit specified by unit_tokens).
    """

    model_id: str
    provider: str
    display_name: str
    input_per_1k: float  # price per 1K prompt/input tokens
    output_per_1k: float  # price per 1K completion/output tokens
    unit_tokens: int = 1000
    currency: str = "USD"


def get_default_pricing() -> Dict[str, ModelPricing]:
    """Return a static pricing table for popular models.

    NOTE: Prices are approximate and may be outdated. Always verify with the
    provider's official pricing page for production use.
    """

    models = [
        # OpenAI
        ModelPricing(
            model_id="openai:gpt-4o-mini",
            provider="OpenAI",
            display_name="gpt-4o-mini",
            input_per_1k=0.0005,
            output_per_1k=0.0015,
        ),
        ModelPricing(
            model_id="openai:gpt-4.1-mini",
            provider="OpenAI",
            display_name="gpt-4.1-mini",
            input_per_1k=0.003,
            output_per_1k=0.006,
        ),
        ModelPricing(
            model_id="openai:gpt-4.1",
            provider="OpenAI",
            display_name="gpt-4.1",
            input_per_1k=0.025,
            output_per_1k=0.075,
        ),
        # Anthropic
        ModelPricing(
            model_id="anthropic:claude-3.5-sonnet",
            provider="Anthropic",
            display_name="Claude 3.5 Sonnet",
            input_per_1k=0.003,
            output_per_1k=0.015,
        ),
        ModelPricing(
            model_id="anthropic:claude-3.5-haiku",
            provider="Anthropic",
            display_name="Claude 3.5 Haiku",
            input_per_1k=0.0008,
            output_per_1k=0.004,
        ),
        # Google
        ModelPricing(
            model_id="google:gemini-1.5-pro",
            provider="Google",
            display_name="Gemini 1.5 Pro",
            input_per_1k=0.0035,
            output_per_1k=0.0105,
        ),
        ModelPricing(
            model_id="google:gemini-1.5-flash",
            provider="Google",
            display_name="Gemini 1.5 Flash",
            input_per_1k=0.00035,
            output_per_1k=0.00105,
        ),
        # DeepSeek (approximate public cloud pricing)
        ModelPricing(
            model_id="deepseek:deepseek-v3",
            provider="DeepSeek",
            display_name="DeepSeek-V3",
            input_per_1k=0.00014,
            output_per_1k=0.00028,
        ),
        ModelPricing(
            model_id="deepseek:deepseek-r1",
            provider="DeepSeek",
            display_name="DeepSeek-R1",
            input_per_1k=0.00055,
            output_per_1k=0.00219,
        ),
    ]

    return {m.model_id: m for m in models}


