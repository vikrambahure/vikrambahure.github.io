"""
Runnable demo for the public Leontief oil-shock code sample.

This script uses a small synthetic input-output matrix. It is meant to show
how the research functions are called, not to reproduce the published India
oil-shock blog results.

Run from the repository root:
    python code_samples/run_leontief_oil_sample.py
"""

from __future__ import annotations

import pandas as pd

from leontief_oil_pass_through import (
    OilShockScenario,
    current_account_sensitivity,
    rank_sector_pressure,
    sector_pass_through,
)


def make_synthetic_india_io() -> tuple[pd.DataFrame, pd.Series]:
    """
    Create a toy input-output matrix and crude-input vector.

    The matrix is stylised and intentionally small. It is not ADB MRIO data
    and should not be compared with the published research-note metrics.
    """
    sectors = [
        "Fertilisers",
        "Synthetic textiles",
        "Specialty chemicals",
        "Aviation",
        "IT services",
        "Banks",
    ]

    a_matrix = pd.DataFrame(
        [
            [0.04, 0.02, 0.04, 0.01, 0.00, 0.00],
            [0.03, 0.05, 0.04, 0.01, 0.01, 0.00],
            [0.05, 0.03, 0.06, 0.02, 0.01, 0.00],
            [0.01, 0.01, 0.02, 0.03, 0.01, 0.00],
            [0.00, 0.01, 0.01, 0.01, 0.04, 0.02],
            [0.00, 0.00, 0.01, 0.01, 0.03, 0.05],
        ],
        index=sectors,
        columns=sectors,
    )

    crude_input_share = pd.Series(
        {
            "Fertilisers": 0.62,
            "Synthetic textiles": 0.48,
            "Specialty chemicals": 0.40,
            "Aviation": 0.38,
            "IT services": 0.03,
            "Banks": 0.02,
        }
    )

    return a_matrix, crude_input_share


def main() -> None:
    a_matrix, crude_input_share = make_synthetic_india_io()
    scenarios = [
        OilShockScenario(name="brent_90", brent_price=90),
        OilShockScenario(name="brent_100", brent_price=100),
    ]

    table = sector_pass_through(a_matrix, crude_input_share, scenarios)
    top_pressure = rank_sector_pressure(table, scenario_name="brent_100", top_n=4)

    print("Public Leontief oil-shock sample")
    print("Synthetic IO data only; does not reproduce the blog results.")
    print()
    print("Top sector pressure at $100 Brent")
    cols = [
        "sector",
        "direct_exposure",
        "indirect_exposure",
        "total_exposure",
        "brent_100_input_cost_pct",
    ]
    print(top_pressure[cols].round(3).to_string(index=False))

    print()
    print(
        "Approx. CAD widening at $100 Brent:",
        f"{current_account_sensitivity(100):.2f}% of GDP",
    )


if __name__ == "__main__":
    main()
