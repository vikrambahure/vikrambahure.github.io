"""
Minimal rates relative-value research sample.

This is a compact public sample of a rates relative-value workflow:
1. validate two yield series,
2. estimate Johansen cointegration,
3. construct a residual,
4. estimate a simple error-correction forecast,
5. trade residual z-score mean reversion only when the ECM agrees,
6. report simple diagnostics.

Dependencies: pandas, numpy, statsmodels.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.vector_ar.vecm import coint_johansen


@dataclass(frozen=True)
class BacktestConfig:
    lookback: int = 252
    entry_z: float = 1.0
    exit_z: float = 0.25
    max_holding_days: int = 120
    cost_per_turnover: float = 0.0001


def prepare_yields(df: pd.DataFrame, italy_col: str, germany_col: str) -> pd.DataFrame:
    """Return a clean two-column yield panel sorted by date."""
    panel = df[[italy_col, germany_col]].copy()
    panel = panel.rename(columns={italy_col: "italy_2y", germany_col: "germany_2y"})
    panel = panel.apply(pd.to_numeric, errors="coerce").dropna()
    panel = panel.sort_index()
    if len(panel) < 300:
        raise ValueError("Need at least 300 observations for this sample workflow.")
    return panel


def johansen_hedge_ratio(panel: pd.DataFrame, det_order: int = 0, k_ar_diff: int = 1) -> float:
    """
    Estimate the Italy/Germany hedge ratio from the leading Johansen vector.

    The vector is normalised on the Italy leg:
        residual = italy_2y - beta * germany_2y
    """
    result = coint_johansen(panel[["italy_2y", "germany_2y"]], det_order, k_ar_diff)
    vector = result.evec[:, 0]
    normalised = vector / vector[0]
    beta = -normalised[1]
    return float(beta)


def build_residual(panel: pd.DataFrame, beta: float) -> pd.Series:
    """Construct the static cointegration residual."""
    residual = panel["italy_2y"] - beta * panel["germany_2y"]
    residual.name = "residual"
    return residual


def rolling_zscore(series: pd.Series, lookback: int) -> pd.Series:
    """Compute rolling z-score using prior-window mean and volatility."""
    mean = series.rolling(lookback).mean().shift(1)
    vol = series.rolling(lookback).std(ddof=0).shift(1)
    return (series - mean) / vol


def estimate_error_correction_forecast(residual: pd.Series, lookback: int) -> pd.Series:
    """
    Estimate a rolling one-step residual-change forecast.

    The model is deliberately compact:
        delta_residual[t] = alpha + lambda * residual[t-1] + error[t]

    A negative lambda means a high residual tends to fall and a low residual
    tends to rise, which is the behaviour needed for mean reversion.
    """
    lagged = residual.shift(1)
    delta = residual.diff()
    forecast = pd.Series(index=residual.index, dtype=float, name="ecm_forecast")

    for end in range(lookback, len(residual)):
        y = delta.iloc[end - lookback : end].dropna()
        x = lagged.reindex(y.index).dropna()
        y = y.reindex(x.index)
        if len(y) < lookback * 0.8:
            continue

        model = sm.OLS(y, sm.add_constant(x)).fit()
        current_x = sm.add_constant(pd.Series([lagged.iloc[end]], index=[residual.index[end]]), has_constant="add")
        forecast.iloc[end] = float(model.predict(current_x).iloc[0])

    return forecast


def make_positions(zscore: pd.Series, ecm_forecast: pd.Series, cfg: BacktestConfig) -> pd.Series:
    """
    Mean-reversion rule:
    - z > entry and ECM forecast is negative: short residual
    - z < -entry and ECM forecast is positive: long residual
    - abs(z) < exit: flat
    - max holding period exits stale trades
    """
    position = 0
    holding_days = 0
    out = []

    for z, forecast in zip(zscore, ecm_forecast):
        if np.isnan(z) or np.isnan(forecast):
            out.append(0)
            continue

        if position == 0:
            if z > cfg.entry_z and forecast < 0:
                position = -1
                holding_days = 0
            elif z < -cfg.entry_z and forecast > 0:
                position = 1
                holding_days = 0
        else:
            holding_days += 1
            if abs(z) < cfg.exit_z or holding_days >= cfg.max_holding_days:
                position = 0
                holding_days = 0

        out.append(position)

    return pd.Series(out, index=zscore.index, name="position")


def backtest_residual_strategy(residual: pd.Series, cfg: BacktestConfig) -> pd.DataFrame:
    """Return daily strategy returns and core columns for review."""
    zscore = rolling_zscore(residual, cfg.lookback)
    ecm_forecast = estimate_error_correction_forecast(residual, cfg.lookback)
    position = make_positions(zscore, ecm_forecast, cfg)

    residual_change = residual.diff()
    gross_return = position.shift(1).fillna(0) * residual_change

    turnover = position.diff().abs().fillna(position.abs())
    cost = turnover * cfg.cost_per_turnover
    net_return = gross_return - cost

    return pd.DataFrame(
        {
            "residual": residual,
            "zscore": zscore,
            "ecm_forecast": ecm_forecast,
            "position": position,
            "gross_return": gross_return,
            "transaction_cost": cost,
            "net_return": net_return,
        }
    )


def performance_summary(results: pd.DataFrame, periods_per_year: int = 252) -> dict[str, float]:
    """Compute a small set of diagnostics suitable for a research note."""
    ret = results["net_return"].dropna()
    if ret.empty or ret.std(ddof=0) == 0:
        raise ValueError("No non-zero return stream to summarise.")

    sharpe = np.sqrt(periods_per_year) * ret.mean() / ret.std(ddof=0)
    cumulative = ret.cumsum()
    drawdown = cumulative - cumulative.cummax()

    return {
        "annualised_sharpe": float(sharpe),
        "total_return_units": float(cumulative.iloc[-1]),
        "max_drawdown_units": float(drawdown.min()),
        "trade_count": float((results["position"].diff().abs() > 0).sum()),
    }


def run_research_sample(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    """Example orchestration function for a two-column rates panel."""
    cfg = BacktestConfig()
    panel = prepare_yields(df, italy_col="italy_2y", germany_col="germany_2y")
    beta = johansen_hedge_ratio(panel)
    residual = build_residual(panel, beta)
    results = backtest_residual_strategy(residual, cfg)
    summary = performance_summary(results)
    summary["johansen_beta"] = beta
    return results, summary
