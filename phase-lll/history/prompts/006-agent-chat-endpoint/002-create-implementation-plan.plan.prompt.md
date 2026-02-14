---
id: 002
title: Create Agent Chat Endpoint Implementation Plan
stage: plan
date: 2026-02-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: 006-agent-chat-endpoint
branch: 006-agent-chat-endpoint
user: Adi
command: /sp.plan
labels: ["plan", "openrouter", "agent", "chat", "function-calling"]
links:
  spec: specs/006-agent-chat-endpoint/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/006-agent-chat-endpoint/plan.md
tests:
  - null
---

## Prompt

/sp.plan

Create: Agent Service, Chat Router, OpenRouter Client Configuration.
Decisions needing documentation: System prompt design, Handling OpenRouter specific headers (HTTP-Referer).
Testing strategy: Use Postman to send JSON payloads and verify DB updates and OpenRouter usage logs.

Technical details:
- Phase 1: Configure `OpenAI` client with OpenRouter Base URL.
- Phase 2: Create the `chat.py` router.
- Phase 3: Implement logic:
    1. Fetch `Conversation`.
    2. Load `Message` history.
    3. Construct payload with System Prompt + History + Tools (from MCP).
    4. Call OpenRouter API.
    5. Handle Tool Calls (execute MCP tool -> send result back to LLM -> get final response).
    6. Save interaction to DB.

## Response snapshot

Created 3-phase implementation plan:

**Phase 1: Configuration** - OpenAI SDK with OpenRouter base_url, system prompt, HTTP-Referer headers
**Phase 2: Router & Schemas** - ChatRequest/ChatResponse Pydantic models, POST /api/chat endpoint
**Phase 3: Agent Logic** - Tool definitions for function calling, tool dispatcher with server-side user_id injection, run_agent() core loop with tool-call iteration, error handling

**Key architectural decisions (3 ADRs):**
- ADR-003: Standard OpenAI SDK over Agents SDK for OpenRouter compatibility
- ADR-004: Server-side user_id injection (never exposed to LLM) for security
- ADR-005: Static system prompt as constant in agent.py

**New files:** agent.py, routers/chat.py, schemas.py
**Modified files:** main.py, requirements.txt

Constitution check passed all 5 principles.

## Outcome

- Impact: Complete implementation plan for agent chat integration
- Tests: Manual Postman testing strategy defined
- Files: 1 file created (plan.md)
- Next prompts: /sp.tasks to generate actionable task list, /sp.adr for documented decisions
- Reflection: Codebase exploration confirmed tool _impl functions are directly reusable; standard OpenAI SDK is the right choice over Agents SDK
