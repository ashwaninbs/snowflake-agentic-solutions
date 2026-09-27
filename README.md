# The Agentic Enterprise on Snowflake — runnable solutions

A solution series accompanying [NorthBay's architecture blueprint](https://northbay-agentic-snowflake.ashwani-ks.chatgpt.site). It uses one fictional enterprise dataset across all installments. No customer information is included.

## Roadmap

| Solution | Demonstration | Status |
| --- | --- | --- |
| 00 | Synthetic enterprise data, ontology, local Streamlit explorer | Runnable |
| 01 | Load into Snowflake and map the ontology to physical data | Planned |
| 02 | Semantic Views and verified business questions | Planned |
| 03 | Cortex Agent with structured and document evidence | Planned |
| 04 | Governed MCP action using a mock service | Planned |
| 05 | Reusable CoWork skill and workflow | Planned |
| 06 | Scheduled intelligence and fresh-data scenarios | Planned |
| 07 | Access control, evaluation, monitoring, and cost | Planned |

Begin with [Solution 00](solutions/00-foundation/README.md). Python dependencies are managed with `uv` and pinned in `uv.lock`. The UI is Streamlit; the later agent solution will target Streamlit in Snowflake's container runtime.

Each installment will include setup, prerequisites, expected results, evaluation questions, and cleanup. Snowflake objects and compute costs are introduced only in installments that require an account.
