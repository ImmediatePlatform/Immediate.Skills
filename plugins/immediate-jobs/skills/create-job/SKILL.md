---
name: create-job
description: Create or update an Immediate.Jobs background job with a source-generated handler, persisted payload contract, stable job identity, execution policy, queue assignment, and host registration. Use only against a verified restorable Immediate.Jobs preview baseline; the package and this skill are not yet stable.
---

# Create an Immediate job

Create durable background work without accidentally changing its persisted contract.

## Workflow

1. Verify that the solution restores a mutually compatible Immediate.Jobs preview package set. Stop and explain the preview dependency if it does not.
2. Inspect nearby handlers, job names, queues, tags, payload conventions, idempotency strategy, and registration code.
3. Read [job-contract.md](references/job-contract.md).
4. Add `[Handler, Job]` to a non-nested `partial` class with exactly one private instance `HandleAsync` method returning non-generic `ValueTask`.
5. Put the request first and `CancellationToken` last. Use `EmptyJobRequest` only for payloadless work.
6. Give production jobs an explicit stable `Name`; treat payload shape, job name, context extractor keys, and queue name as persisted schema.
7. Select retry, timeout, concurrency, backoff, overlap, and queue policies deliberately. Make the handler idempotent for at-least-once delivery.
8. Import the project's root namespace. Register handlers and generated `AddXxxJobs(tags)` with the same tags, then configure runtime and storage from the returned builder. Handler registration adds the needed concrete behavior dependencies. Run the full host so workers execute.
9. Build and add a deterministic test that covers success plus the important retry or idempotency path.

## Guardrails

- Do not claim exactly-once processing or invent a transactional outbox; Immediate.Jobs provides at-least-once delivery.
- Do not rename a production job merely to match a class rename. Existing durable records use the persisted name.
- Do not store unsupported or unbounded object graphs in payloads. Payloads use source-generated System.Text.Json metadata.
- Do not add a queue definition without assigning a job to it; `IJOB0016` reports the unused queue.
- Do not assume `AddXxxJobs` registers handlers; call both generated registration methods.

## Handoff

Report the preview package versions, persisted name and payload, queue/policy choices, idempotency boundary, registration path, and test evidence.
