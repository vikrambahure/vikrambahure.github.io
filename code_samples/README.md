# Public Python Code Samples

These are public Python samples for viewing. They show the structure of the analysis code behind two research workflows, using simplified examples and synthetic data.

The samples are not intended to reproduce the published research-note results. The research notes use fuller datasets and a broader analysis pipeline. These files are only a compact view of implementation style.

## Files

- `johansen_ecm_btp_schatz.py`  
  A compact rates relative-value workflow: input validation, Johansen cointegration test, residual construction, z-score signal, and simple ECM-style backtest.

- `run_btp_schatz_sample.py`  
  A runnable demo using synthetic yield data. It shows how the functions are called and prints a small summary.

- `leontief_oil_pass_through.py`  
  A compact input-output workflow: matrix validation, Leontief inverse, crude shock scenarios, sector pass-through, and current-account sensitivity.

- `run_leontief_oil_sample.py`  
  A runnable demo using a synthetic input-output matrix. It shows how the functions are called and prints a small sector-pressure table.

These are examples, not production trading systems and not investment advice.

## Run

From the repository root:

```powershell
python code_samples/run_btp_schatz_sample.py
python code_samples/run_leontief_oil_sample.py
```
