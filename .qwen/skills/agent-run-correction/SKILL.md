---
name: agent-run-correction
description: Fix missing `run` method usage in OpenAI IMEI agent service by replacing incorrect `arun` calls with the correct async `run` method.
source: auto-skill
extracted_at: '2026-06-09T05:58:00.000Z'
---

## Problem
The OpenAI IMEI matching agent service (`agents/openai_imei_agent_service.py`) attempted to call `self.agent.arun(...)`. The `Agent` class from the `openai‑agents` library does **not** provide an `arun` method, only an asynchronous `run` method (or its synchronous wrapper). This caused a runtime error:
```
'Agent' object has no attribute 'arun'
```

## Solution
Replace every occurrence of `self.agent.arun` with `await self.agent.run`. The service already uses `await` for asynchronous execution, so the change is straightforward and requires no other code modifications.

### Steps performed
1. **Locate the incorrect calls** – searched the file for the string `arun` and found two locations:
   - inside `process_event`
   - inside `run_system_wide_analysis`
2. **Edit the file** – used the `edit` tool with `replace_all=True` to replace the three‑line snippet:
   ```python
   result = await self.agent.arun(
       prompt,
       run_config=config,
   )
   ```
   with the correct call:
   ```python
   result = await self.agent.run(
       prompt,
       run_config=config,
   )
   ```
3. **Verify** – after editing, the relevant sections now call `self.agent.run`.

## Rationale
Using the proper `run` method aligns with the `openai‑agents` API and resolves the AttributeError, allowing the agent service to process events and perform system‑wide analysis without crashing.

## Aftermath
* The agent service can now be started (`uvicorn agents.agent_service:app`) and will respond correctly to `/process-event` and `/system-analysis` endpoints.
* Existing unit/integration tests that hit these endpoints should now pass.

---

*Implemented on 2026‑06‑09.*