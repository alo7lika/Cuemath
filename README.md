# Cuemath Tutor Hiring Assignment

The work is separated by assignment part. This is the only README; run instructions for every task are here. The four-page summary is at the top level; code, tests, and outputs are grouped below. Supplied applicant data and inbox are intentionally not copied into this package. Use the original CSVs locally when running the scripts.

## Folder map

- `Task_A/` - reproducible data analysis and its run instructions.
- `Task_B/` - repaired weekly report and tests.
- `Task_C/` - OpenAI API agent, expected replies, live-run checkpoint, and tests.
- `Task_D/` - November staffing calculation and Monday checklist.
- `Summary of the work.pdf` - concise four-part submission document.

## Task A - Data analysis

Run with Python 3 and no third-party packages:

```bash
python Task_A/analysis.py path/to/candidates.csv
```

The script prints monthly funnel counts, immediate AI pass rates by version and device, and observed source conversion. The chart and written interpretation are in `assignment_summary.pdf`. September induction conversion is right-censored at the 5 October data cutoff; compare fixed-age signup cohorts before treating the monthly snapshot as final.

## Task B - Weekly report repair

```bash
python Task_B/weekly_report.py path/to/candidates.csv
python -m unittest discover -s Task_B -p 'test_*.py'
```

`facebook` maps to `Meta`; unknown or blank source values remain visible rather than stopping the report. AI pass rate is passes divided by attempts. CET pass rate is CET passes divided by AI passers.

## Task C - Applicant email agent

The agent uses OpenAI Chat Completions tool calling, and the model decides whether to call `lookup_candidate`. The local lookup is read-only and code-limited to the candidate ID on the email. It writes draft decisions to CSV; it does not send email.

```powershell
$env:OPENAI_API_KEY = "your-api-key"
$env:OPENAI_MODEL = "gpt-5.4-mini"
python Task_C/agent.py --candidates path/to/candidates.csv --inbox path/to/inbox.csv --policy path/to/policy.md --output Task_C/replies_model_run.csv --limit 15
python -m unittest discover -s Task_C -p 'test_*.py'
```

ChatGPT subscription access and API quota are separate. Completed replies are checkpointed after each email. Rerunning skips completed message IDs; a persistent rate limit or billing/quota error stops the run and preserves the checkpoint. `--limit N` caps new messages per run.

`Task_C/replies.csv` contains a manually policy-checked expected answer for each sample email; it is not model output. An API key was configured for the attempt in this environment, but DNS/network access failed before OpenAI returned a response. Thus 0/15 messages were model-processed and the current quota/rate limit could not be measured. `Task_C/replies_model_run.csv` is the empty checkpoint from that attempt. Rerun from a network that can reach the API to measure available quota.

The full candidate file is not sent to the model. Only the requested sender's status fields are returned. Email text is treated as untrusted, and the code guard prevents cross-applicant lookup.

## Task D - Operations plan

See `Task_D/operations_plan.md` for the weekly signup and interview estimates, capacity options, selected approach, and Monday checklist.

## Interview demo

1. Run the tests in `Task_B`, then run the report on the supplied candidate CSV. Point out the `facebook` alias, safe handling of unknown labels, and the explicit rate denominators.
2. Add an `instagram` alias to `Meta` in `Task_B/weekly_report.py`, rerun the report, and rerun the tests.
3. In `Task_C/agent.py`, show the sender-ID guard on `lookup_for_email`: a message asking for a friend's ID cannot retrieve that record.
4. If the API is reachable and quota is available, run the agent with `--limit 1`, inspect its checkpoint, then run again with `--limit 15` to show resume behavior. `Task_C/replies.csv` is a human-checked expected-output baseline, not model-generated output. The attempted live API run here completed 0/15 because DNS/network access failed before an API response; no rate limit could be measured.
