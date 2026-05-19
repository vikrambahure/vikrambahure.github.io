---
layout: single
title: "Code"
permalink: /code/
---

The full `chokepointmacro` research stack is private. The files below are public, recruiter-readable Python samples that mirror the style of the private work without exposing private data, credentials, broker integrations, or full project internals.

These samples do **not** reproduce the published BTP-Schatz research-note results. The published results use private data, private run artefacts, and the fuller private research pipeline. The public files are intentionally small review samples.

## Python Sample

**[Johansen / ECM rates relative-value sample](/code_samples/johansen_ecm_btp_schatz.py)**

A compact rates workflow covering input validation, Johansen hedge-ratio estimation, residual construction, an error-correction forecast, rolling z-score signal generation, transaction-cost handling, and simple performance diagnostics.

**[Runnable synthetic-data demo](/code_samples/run_btp_schatz_sample.py)**

A small script that generates stylised synthetic Italy/Germany 2Y yield data, runs the sample workflow, and prints summary diagnostics. It is for code review only, not research replication.

**[Leontief oil-shock pass-through sample](/code_samples/leontief_oil_pass_through.py)**

A compact input-output workflow covering matrix validation, Leontief inverse computation, crude-price shock scenarios, sector pass-through, and current-account sensitivity.

**[Runnable synthetic IO demo](/code_samples/run_leontief_oil_sample.py)**

A small script that generates a stylised synthetic input-output matrix, runs the oil-shock workflow, and prints a sector-pressure table. It is for code review only, not research replication.

Run locally from the repository root:

```powershell
python code_samples/run_btp_schatz_sample.py
python code_samples/run_leontief_oil_sample.py
```

## Review Notes

The sample is intentionally short. It is designed to show how I structure research code:

- pure functions where possible,
- explicit assumptions,
- typed configuration objects,
- readable orchestration,
- separation between model logic and reporting,
- no hidden credentials or external state.

The public research notes provide the written output; the code sample provides a quick view of implementation style.
