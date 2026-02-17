from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Optional

from .pricing import ModelPricing, get_default_pricing


@dataclass
class CostBreakdown:
    model_id: str
    provider: str
    display_name: str
    currency: str
    prompt_tokens_per_call: int
    completion_tokens_per_call: int
    calls_per_month: int
    total_prompt_tokens: int
    total_completion_tokens: int
    input_cost: float
    output_cost: float

    @property
    def total_cost(self) -> float:
        return self.input_cost + self.output_cost


def _ensure_pricing_table(
    pricing_table: Optional[Mapping[str, ModelPricing]]
) -> Mapping[str, ModelPricing]:
    return pricing_table or get_default_pricing()


def estimate_for_model(
    prompt_tokens: int,
    completion_tokens: int,
    calls_per_month: int,
    model: ModelPricing,
) -> CostBreakdown:
    total_prompt = prompt_tokens * calls_per_month
    total_completion = completion_tokens * calls_per_month

    input_cost = (total_prompt / model.unit_tokens) * model.input_per_1k
    output_cost = (total_completion / model.unit_tokens) * model.output_per_1k

    return CostBreakdown(
        model_id=model.model_id,
        provider=model.provider,
        display_name=model.display_name,
        currency=model.currency,
        prompt_tokens_per_call=prompt_tokens,
        completion_tokens_per_call=completion_tokens,
        calls_per_month=calls_per_month,
        total_prompt_tokens=total_prompt,
        total_completion_tokens=total_completion,
        input_cost=input_cost,
        output_cost=output_cost,
    )


def estimate_all(
    prompt_tokens: int,
    completion_tokens: int,
    calls_per_month: int,
    pricing_table: Optional[Mapping[str, ModelPricing]] = None,
) -> Dict[str, CostBreakdown]:
    """Estimate monthly cost for all models in the pricing table."""
    table = _ensure_pricing_table(pricing_table)
    return {
        model_id: estimate_for_model(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            calls_per_month=calls_per_month,
            model=model,
        )
        for model_id, model in table.items()
    }


def estimate_from_config(
    config: Mapping,
    pricing_table: Optional[Mapping[str, ModelPricing]] = None,
) -> Dict[str, CostBreakdown]:
    """Estimate cost from a simple YAML/JSON-style config mapping.

    Expected config keys:
      - prompt_tokens: int
      - completion_tokens: int
      - calls_per_month: int
    """
    try:
        prompt_tokens = int(config["prompt_tokens"])
        completion_tokens = int(config["completion_tokens"])
        calls_per_month = int(config["calls_per_month"])
    except KeyError as exc:
        raise ValueError(f"Missing required config key: {exc}") from exc
    except (TypeError, ValueError) as exc:
        raise ValueError("prompt_tokens, completion_tokens and calls_per_month must be integers") from exc

    if prompt_tokens < 0 or completion_tokens < 0 or calls_per_month < 0:
        raise ValueError("prompt_tokens, completion_tokens and calls_per_month must be non-negative")

    return estimate_all(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        calls_per_month=calls_per_month,
        pricing_table=pricing_table,
    )


