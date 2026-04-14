# LinkedIn Alert Intelligence Agent

This is a Python MVP for turning LinkedIn job alert emails into one ranked daily digest. It ingests LinkedIn alert emails, normalizes the job records, deduplicates postings across multiple alerts, scores them against your preferences, stores history in SQLite, and renders an HTML digest that can also be sent by email.

## What is implemented

- Filesystem intake for `.eml` files so the pipeline is runnable locally right now.
- Local Gmail OAuth flow with refresh-token persistence for repeatable daily runs.
- Gmail API intake using either the saved OAuth token or a one-off bearer token fallback.
- Optional Gmail checkpointing with a processed label when you grant `gmail.modify`.
- Email parsing for LinkedIn alert HTML/text into structured job records.
- Normalization for titles, locations, work mode hints, and canonical job URLs.
- SQLite persistence for alerts, jobs, scores, and digests.
- Deterministic ranking with configurable profile rules in [profile.json](/Users/michaelworkman/Desktop/LinkedIn%20job%20search/profile.json).
- Optional OpenAI-based rationale refinement using the Responses API when `OPENAI_REASONER_ENABLED=true`.
- HTML digest generation plus SMTP email delivery when SMTP settings are configured.

## Project layout

- Source code lives in [src/linkedin_alert_agent](/Users/michaelworkman/Desktop/LinkedIn%20job%20search/src/linkedin_alert_agent).
- A sample alert email lives in [examples/data/sample-linkedin-alert.eml](/Users/michaelworkman/Desktop/LinkedIn%20job%20search/examples/data/sample-linkedin-alert.eml).
- Your scoring profile lives in [profile.json](/Users/michaelworkman/Desktop/LinkedIn%20job%20search/profile.json).

## Running it

Use the guided setup if you want the app to ask you plain-English questions instead of editing config by hand:

```bash
PYTHONPATH=src python3 -m linkedin_alert_agent setup
PYTHONPATH=src python3 -m linkedin_alert_agent status
```

Use the local sample email:

```bash
PYTHONPATH=src python3 -m linkedin_alert_agent run --dry-run
```

Point at a different folder of `.eml` files:

```bash
PYTHONPATH=src python3 -m linkedin_alert_agent run --dry-run --source filesystem --input-dir /path/to/eml-files
```

Use Gmail API mode:

```bash
export SOURCE_MODE=gmail
export GMAIL_CLIENT_SECRETS_PATH=secrets/google-oauth-client.json
export GMAIL_LABEL_NAMES='LinkedIn Alerts'
export GMAIL_QUERY='from:(jobalerts-noreply@linkedin.com OR jobs-noreply@linkedin.com) newer_than:2d'
PYTHONPATH=src python3 -m linkedin_alert_agent gmail-auth
PYTHONPATH=src python3 -m linkedin_alert_agent gmail-labels
PYTHONPATH=src python3 -m linkedin_alert_agent run --dry-run
```

Bearer token fallback:

```bash
export SOURCE_MODE=gmail
export GMAIL_ACCESS_TOKEN=your-oauth-bearer-token
export GMAIL_QUERY='from:(jobalerts-noreply@linkedin.com OR jobs-noreply@linkedin.com) newer_than:2d'
PYTHONPATH=src python3 -m linkedin_alert_agent run --dry-run
```

When you are ready to email the digest, set the SMTP variables from [.env.example](/Users/michaelworkman/Desktop/LinkedIn%20job%20search/.env.example) and run without `--dry-run`.

## Gmail setup

1. Create a Google Cloud project and enable the Gmail API.
2. Create an OAuth client for a desktop app and download the client JSON.
3. Save that JSON to [secrets/google-oauth-client.json](/Users/michaelworkman/Desktop/LinkedIn%20job%20search/secrets/google-oauth-client.json) or point `GMAIL_CLIENT_SECRETS_PATH` at it.
4. Optionally create a Gmail label such as `LinkedIn Alerts` and route LinkedIn alert emails into it.
5. Run `PYTHONPATH=src python3 -m linkedin_alert_agent gmail-auth`.
6. Verify labels with `PYTHONPATH=src python3 -m linkedin_alert_agent gmail-labels`.
7. Run the pipeline with `SOURCE_MODE=gmail`.

If you want the pipeline to mark processed Gmail messages read, set `GMAIL_MARK_READ=true` and re-run `gmail-auth` so the saved token includes `gmail.modify`.
If you also want Gmail-side checkpointing, set `GMAIL_PROCESSED_LABEL_NAME='LinkedIn Digest Processed'` and re-run `gmail-auth --allow-modify` so the saved token includes `gmail.modify`.

## Output

- SQLite database: `data/linkedin_alerts.sqlite3`
- HTML digest: `output/linkedin-digest-YYYY-MM-DD.html`
- Failed parses: `output/failed/`

## Profile tuning

Edit [profile.json](/Users/michaelworkman/Desktop/LinkedIn%20job%20search/profile.json) to change:

- target titles
- target locations
- positive and avoid keywords
- company quality signals
- classification thresholds

## Scheduling

For a daily morning run, add a cron entry such as:

```cron
0 7 * * * cd /Users/michaelworkman/Desktop/LinkedIn\ job\ search && PYTHONPATH=src /usr/bin/python3 -m linkedin_alert_agent run
```

## GitHub Actions

If you want the digest to arrive even when your laptop is off, use the included GitHub Actions workflow at [.github/workflows/weekday-digest.yml](/Users/michaelworkman/Desktop/LinkedIn%20job%20search/.github/workflows/weekday-digest.yml).

What it does:

- runs every weekday at 7:00 AM Eastern
- also supports a manual "Run workflow" test from GitHub
- restores the SQLite history file from a dedicated `linkedin-digest-state` branch
- validates the saved Gmail token before processing so missing send scope fails fast
- persists the SQLite history back to that state branch after a successful run
- uploads the rendered digest HTML as a workflow artifact after each run

Before you enable it, push this repo to GitHub and add these repository secrets:

- `DIGEST_TO_EMAIL`
  Use `michael.w.workman@gmail.com`
- `GMAIL_CLIENT_SECRETS_JSON`
  Paste the full contents of your local [secrets/google-oauth-client.json](/Users/michaelworkman/Desktop/LinkedIn%20job%20search/secrets/google-oauth-client.json)
- `GMAIL_TOKEN_JSON`
  Paste the full contents of your local [secrets/google-token.json](/Users/michaelworkman/Desktop/LinkedIn%20job%20search/secrets/google-token.json)
  This token should include `gmail.readonly` plus `gmail.send`. Add `gmail.modify` only if you later enable message-state changes such as Gmail-side checkpoint labels or marking messages read.
- `OPENAI_API_KEY`
  Optional. Add this only if you want the optional AI rationale refinement in GitHub too.

After those secrets are added:

1. Push the repo to GitHub.
2. Open the `Actions` tab in GitHub.
3. Open `Weekday LinkedIn Digest`.
4. Click `Run workflow` once for a live test.
5. Confirm the run creates or updates the `linkedin-digest-state` branch.
6. Leave the workflow enabled for weekday 7:00 AM runs.

The workflow no longer relies on the GitHub Actions cache for history. The dedicated `linkedin-digest-state` branch is the durable checkpoint for the SQLite state. Gmail-side processed labels remain available as an optional extra layer if you later decide to grant `gmail.modify`.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
