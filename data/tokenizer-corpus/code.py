"""Fixed code sample used for tokenizer normalisation measurements."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ServingConfig:
    gpu_hourly_rate: float
    gpu_count: int
    throughput_tok_per_s: float
    utilization: float

    def validate(self) -> None:
        if not 0.0 < self.utilization <= 1.0:
            raise ValueError(f"utilization out of range: {self.utilization}")
        if self.throughput_tok_per_s <= 0:
            raise ValueError("throughput must be positive")


def cost_per_million_tokens(cfg: ServingConfig) -> float:
    """Return USD per 1M output tokens for a self-hosted deployment."""
    cfg.validate()
    tokens_per_hour = cfg.throughput_tok_per_s * 3600.0 * cfg.utilization
    hourly_cost = cfg.gpu_hourly_rate * cfg.gpu_count
    return (hourly_cost / tokens_per_hour) * 1_000_000


def break_even_tokens(api_price: float, cfg: ServingConfig) -> float | None:
    self_hosted = cost_per_million_tokens(cfg)
    if self_hosted >= api_price:
        return None
    monthly_fixed = cfg.gpu_hourly_rate * cfg.gpu_count * 24 * 30
    delta = api_price - self_hosted
    return math.ceil(monthly_fixed / delta) if delta > 0 else None


if __name__ == "__main__":
    config = ServingConfig(2.99, 8, 12000.0, 0.30)
    print(f"{cost_per_million_tokens(config):.2f}")
