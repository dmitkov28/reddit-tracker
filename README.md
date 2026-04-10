# Reddit Tracker

[![Deploy Infra](https://github.com/dmitkov28/reddit-tracker/actions/workflows/deploy-infra.yaml/badge.svg)](https://github.com/dmitkov28/reddit-tracker/actions/workflows/deploy-infra.yaml)
[![Build and Push Fetcher](https://github.com/dmitkov28/reddit-tracker/actions/workflows/build-fetcher.yaml/badge.svg)](https://github.com/dmitkov28/reddit-tracker/actions/workflows/build-fetcher.yaml)
[![Build and Push Loader](https://github.com/dmitkov28/reddit-tracker/actions/workflows/build-loader.yaml/badge.svg)](https://github.com/dmitkov28/reddit-tracker/actions/workflows/build-loader.yaml)
[![Test Fetcher](https://github.com/dmitkov28/reddit-tracker/actions/workflows/test-fetcher.yaml/badge.svg)](https://github.com/dmitkov28/reddit-tracker/actions/workflows/test-fetcher.yaml)

A serverless ETL pipeline that scrapes Reddit daily — collecting threads, comments, and subreddit metadata — and loads the data into a PostgreSQL database. Orchestrated by AWS Step Functions and triggered on a daily schedule via EventBridge.

## Architecture

![Step Function Graph](.github/assets/tracker_graph.svg)

The pipeline runs in three sequential stages:

### 1. Fetch (Extract)

An EventBridge rule triggers the Step Function once per day. The first stage reads a list of subreddits from `s3://<<bucket>>/subreddits.json` and fans out using a distributed Map state (up to 20 concurrent executions). Each iteration invokes the **Fetcher Lambda**, which:

- Scrapes threads, comments, and subreddit metadata from Reddit's JSON API via `httpx`
- Writes raw JSON to S3, partitioned by `year/month/day` (e.g. `threads/year=2026/month=4/day=10/thread=abc123.json`)
- Paginates backwards until it reaches posts older than 2 days

### 2. Transform

Three Athena named queries run in parallel, each reading the raw JSON data from S3 (via Glue Catalog tables with partition projection) and writing deduplicated, cleaned Parquet files back to S3:

| Query | Description |
|---|---|
| `TodaySubreddits` | Extracts today's subreddit metadata |
| `LastTwoDaysFetchedThreads` | Joins threads with subreddits, deduplicates by thread ID |
| `LastTwoDaysComments` | Extracts comments from the last 2 days |

The Step Function polls each query's execution status in a loop (wait 5s → check → repeat) until it succeeds or fails.

### 3. Load

The **Loader Lambda** reads the Parquet output from Athena using DuckDB (with the `httpfs` and `postgres` extensions) and upserts data directly into PostgreSQL:

- `subreddits` and `subreddit_subscribers` — subscriber counts tracked over time
- `threads` — deduplicated by primary key (`ON CONFLICT DO NOTHING`)
- `comments` — deduplicated by primary key, loaded after threads (foreign key dependency)

Threads and comments are loaded sequentially within a parallel branch to respect the `threads → comments` foreign key constraint, while subreddits are loaded independently in a separate branch.

## Idempotency

The pipeline is safe to re-run for the same day without producing duplicates:

- **Fetcher**: Writes to deterministic S3 keys based on entity ID and date partition (`threads/year=.../thread={id}.json`). Re-fetching the same thread overwrites the same key.
- **Athena**: `UNLOAD` queries write to date-partitioned paths. Re-running overwrites the same partition.
- **Loader**: All upserts use `ON CONFLICT DO NOTHING` (threads, comments, subreddits) or check for existing `(subreddit_id, date)` pairs (subscriber counts) before inserting.
- **S3 lifecycle**: Raw data and Athena outputs expire after 14 days, keeping storage bounded.

## Project Structure

```
├── fetcher/                  # Fetcher Lambda (Python, httpx, boto3)
│   └── src/
│       ├── reddit_client/    # Reddit JSON API client
│       ├── services/         # Orchestration (collect threads/comments/subreddits)
│       ├── storer/           # S3 storage abstraction
│       └── model.py          # Data models (Thread, Comment, Subreddit)
├── loader/                   # Loader Lambda (Python, DuckDB, psycopg2)
│   └── src/
│       ├── services.py       # Upsert queries (DuckDB → PostgreSQL)
│       └── dependencies.py   # DuckDB connection setup
├── db_schema/                # Alembic migrations (PostgreSQL)
│   └── migrations/versions/  # subreddits, subreddit_subscribers, threads, comments
├── infrastructure/           # Terraform (AWS)
│   ├── step_function.asl.json
│   ├── lambda.tf
│   ├── athena.tf
│   ├── glue.tf
│   ├── s3.tf
│   ├── ecr.tf
│   └── eventbridge.tf
└── .github/workflows/        # CI/CD
    ├── test-fetcher.yaml     # Lint + test
    ├── build-fetcher.yaml    # Build & push to ECR
    ├── deploy-fetcher.yaml   # Update Lambda image
    ├── build-loader.yaml     # Build, push & deploy
    └── deploy-infra.yaml     # Terraform plan + apply
```

## Tech Stack

| Layer | Technology |
|---|---|
| Runtime | Python 3.13 |
| Orchestration | AWS Step Functions (JSONata) |
| Compute | AWS Lambda (container images, arm64) |
| Storage | S3 (raw JSON + Parquet) |
| Query Engine | Athena + Glue Catalog (partition projection) |
| Loading | DuckDB (in-memory, `httpfs` + `postgres` extensions) |
| Database | PostgreSQL |
| IaC | Terraform (Terraform Cloud backend) |
| CI/CD | GitHub Actions (OIDC auth) |
| Packaging | uv, Docker |

## Use Cases

The PostgreSQL database serves as a ready-made backend for analytics and dashboards. Since data is deduplicated and loaded daily, it plugs directly into tools like:

- **Looker Studio** / **Metabase** / **Grafana** — track subreddit growth, posting trends, and comment activity over time
- **Subreddit benchmarking** — compare subscriber counts, post volume, and engagement across communities
- **Content monitoring** — surface trending threads or authors within tracked subreddits
- **Historical analysis** — subscriber time-series data (`subreddit_subscribers`) enables growth-rate and seasonality analysis
