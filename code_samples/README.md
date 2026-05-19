# Public Python Code Samples

This folder contains short, recruiter-readable extracts that mirror the style of the private `chokepointmacro` research stack without exposing private data, credentials, broker code, or full project internals.

Important: these samples do not reproduce the published research-note results. The blog results use private data, private run artefacts, and the fuller private research pipeline. The public files are intentionally small review samples.

The samples are intended to show:

- clean research functions,
- explicit assumptions,
- reproducible analysis flow,
- no hidden state,
- code that can be reviewed quickly.

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
