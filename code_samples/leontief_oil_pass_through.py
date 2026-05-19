"""
Minimal input-output pass-through research sample.

This mirrors the structure of a private oil-shock workflow without private
data or full project internals:
1. validate an input-output coefficient matrix,
2. compute the Leontief inverse,
3. apply crude-price scenarios,
4. estimate sector input-cost pressure,
5. estimate a simple current-account sensitivity.

Dependencies: pandas, numpy.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class OilShockScenario:
    name: str
    brent_price: float
    baseline_price: float = 67.0

    @property
    def crude_return(self) -> float:
        return self.brent_price / self.baseline_price - 1.0


def validate_io_matrix(a_matrix: pd.DataFrame) -> pd.DataFrame:
    """Validate a square technical-coefficient matrix."""
    if a_matrix.empty:
        raise ValueError("Input-output matrix is empty.")
    if a_matrix.shape[0] != a_matrix.shape[1]:
        raise ValueError("Input-output matrix must be square.")
    if list(a_matrix.index) != list(a_matrix.columns):
        raise ValueError("Rows and columns must use the same sector order.")
    return a_matrix.astype(float)


def leontief_inverse(a_matrix: pd.DataFrame) -> pd.DataFrame:
    """Compute the price-side Leontief inverse: (I - A')^-1."""
    a_matrix = validate_io_matrix(a_matrix)
    identity = np.eye(len(a_matrix))
    inverse = np.linalg.inv(identity - a_matrix.to_numpy().T)
    return pd.DataFrame(inverse, index=a_matrix.index, columns=a_matrix.columns)


def sector_pass_through(
    a_matrix: pd.DataFrame,
    crude_input_share: pd.Series,
    scenarios: list[OilShockScenario],
) -> pd.DataFrame:
    """
    Estimate crude-shock pass-through for each sector and scenario.

    crude_input_share is a sector-indexed vector measuring direct crude-linked
    input exposure. The Leontief inverse propagates the shock through the
    intermediate-input network.
    """
    inverse = leontief_inverse(a_matrix)
    crude_input_share = crude_input_share.reindex(a_matrix.index).fillna(0).astype(float)

    total_exposure = inverse @ crude_input_share
    direct_exposure = crude_input_share
    indirect_exposure = total_exposure - direct_exposure

    rows = []
    for sector in a_matrix.index:
        row = {
            "sector": sector,
            "direct_exposure": direct_exposure.loc[sector],
            "indirect_exposure": indirect_exposure.loc[sector],
            "total_exposure": total_exposure.loc[sector],
        }
        for scenario in scenarios:
            row[f"{scenario.name}_input_cost_pct"] = (
                100 * total_exposure.loc[sector] * scenario.crude_return
            )
        rows.append(row)

    return pd.DataFrame(rows).sort_values("total_exposure", ascending=False)


def current_account_sensitivity(
    brent_price: float,
    baseline_price: float = 67.0,
    sensitivity_pct_gdp_per_10_dollars: float = 0.4,
) -> float:
    """Approximate current-account deficit widening as percent of GDP."""
    dollars_above_baseline = brent_price - baseline_price
    return (dollars_above_baseline / 10.0) * sensitivity_pct_gdp_per_10_dollars


def rank_sector_pressure(table: pd.DataFrame, scenario_name: str, top_n: int = 5) -> pd.DataFrame:
    """Return the sectors with the largest scenario input-cost pressure."""
    column = f"{scenario_name}_input_cost_pct"
    if column not in table.columns:
        raise KeyError(f"Scenario column not found: {column}")
    return table.sort_values(column, ascending=False).head(top_n)
