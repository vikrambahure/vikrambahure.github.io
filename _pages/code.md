---
layout: single
title: "Code"
permalink: /code/
---

These are public Python samples for viewing. They show the structure of the analysis code behind two research workflows, using simplified examples and synthetic data.

The samples are not intended to reproduce the published research-note results. The research notes use fuller datasets and a broader analysis pipeline. These files are only a compact view of implementation style.

## Python Samples

**[Johansen / ECM rates relative-value sample](/code_samples/johansen_ecm_btp_schatz.py)**

A compact rates workflow covering input validation, Johansen hedge-ratio estimation, residual construction, an error-correction forecast, rolling z-score signal generation, transaction-cost handling, and simple performance diagnostics.

**[Runnable synthetic-data demo](/code_samples/run_btp_schatz_sample.py)**

A small script that generates stylised synthetic Italy/Germany 2Y yield data, runs the sample workflow, and prints summary diagnostics.

**[Leontief oil-shock pass-through sample](/code_samples/leontief_oil_pass_through.py)**

A compact input-output workflow covering matrix validation, Leontief inverse computation, crude-price shock scenarios, sector pass-through, and current-account sensitivity.

**[Runnable synthetic IO demo](/code_samples/run_leontief_oil_sample.py)**

A small script that generates a stylised synthetic input-output matrix, runs the oil-shock workflow, and prints a sector-pressure table.

Run locally from the repository root:

```powershell
python code_samples/run_btp_schatz_sample.py
python code_samples/run_leontief_oil_sample.py
```

## What To Look For

- clean research functions,
- explicit assumptions,
- typed configuration objects,
- readable orchestration,
- separation between model logic and reporting,
- no hidden external state.
