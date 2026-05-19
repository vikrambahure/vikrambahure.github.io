"""
Runnable demo for the public Johansen / ECM code sample.

This script uses synthetic yield data. It is meant to show how the research
functions are called, not to reproduce the published BTP-Schatz blog results.

Run from the repository root:
    python code_samples/run_btp_schatz_sample.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from johansen_ecm_btp_schatz import run_research_sample


def make_synthetic_btp_schatz_data(n_obs: int = 900, seed: int = 42) -> pd.DataFrame:
    """
    Create a small synthetic two-yield panel with a shared stochastic trend.

    The generated series are intentionally stylised. They are not market data
    and should not be compared with the published research-note metrics.
    """
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2020-01-01", periods=n_obs)

    common_policy_trend = np.cumsum(rng.normal(0.0, 0.018, n_obs))
    mean_reverting_spread = np.zeros(n_obs)

    for t in range(1, n_obs):
        mean_reverting_spread[t] = (
            0.96 * mean_reverting_spread[t - 1]
            + rng.normal(0.0, 0.035)
        )

    germany_2y = common_policy_trend + rng.normal(0.0, 0.01, n_obs)
    italy_2y = 1.04 * germany_2y + mean_reverting_spread

    return pd.DataFrame(
        {
            "italy_2y": italy_2y,
            "germany_2y": germany_2y,
        },
        index=dates,
    )


def main() -> None:
    sample = make_synthetic_btp_schatz_data()
    results, summary = run_research_sample(sample)

    print("Public Johansen / ECM sample")
    print("Synthetic data only; does not reproduce the blog results.")
    print()
    print("Summary")
    for key, value in summary.items():
        print(f"{key}: {value:.4f}")

    print()
    print("Latest rows")
    print(results.tail(5).round(4).to_string())


if __name__ == "__main__":
    main()
