# Module 07: Deployment

## The concept

Everything so far has run on localhost. This module takes the same stack to a real, reachable deployment, because 'it works on my machine' is not the same skill as 'it works when someone else has to run it'.

## Why this module doesn't just say 'deploy to Kubernetes'

Most learning resources either stop at localhost or jump straight to a full Kubernetes cluster, skipping the realistic middle ground most small teams and side projects actually use: a single managed host running Docker Compose, or a PaaS like Render/Railway/Fly.io. This module covers that middle ground, and points to the pipeline-cost-observatory and data-governance-gateway projects in this same GitHub account for real Helm chart / Kubernetes examples once you're ready for that.

## Option 1: a single VM with Docker Compose (closest to what you already know)

1. Provision any small VM (a $5-6/month tier from any provider works).
2. Install Docker + Docker Compose on it.
3. Copy this repo's root docker-compose.yml and the modules/ folder to the VM.
4. docker compose up -d.
5. Put a reverse proxy (Caddy or nginx) in front of port 8080 (Airflow) and 8501 if you add module 06's metrics dashboard, with TLS - never expose Airflow's default UI directly to the internet without at least changing the default admin/admin credentials.

## Option 2: Render / Railway (no server management)

These platforms run a single container well but don't run multi-service Docker Compose stacks natively - so for this option, deploy just the piece that needs to be reachable (e.g. a small FastAPI/Streamlit status dashboard reading from metrics.jsonl or the warehouse), and keep Postgres as their managed database offering rather than self-hosting it. This is the same pattern the pipeline-cost-observatory project uses - see that repo's render.yaml for a concrete, working example you can copy.

## What 'real deployment' changes about the pipeline itself

Secrets (API tokens, DB passwords) move from hardcoded docker-compose.yml values to the platform's secret manager or environment variables injected at deploy time. Logging (module 06) stops being a local file and starts being something you'd ship to a real aggregator. Someone other than you needs to be able to redeploy from the README alone - which is the actual test of whether your documentation is good enough.

## Exercise

1. Pick Option 1 or 2 and actually deploy this course's stack somewhere reachable over the internet, even temporarily.
2. Write down, in your own words, what broke that didn't break locally - there is almost always something, and understanding why is most of the value of this exercise.

You've now been through the full path from a raw API to a real deployment. Go back to the root [README](../../README.md) for what to do next.
