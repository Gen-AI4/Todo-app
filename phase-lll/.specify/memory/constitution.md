<!--
Sync Impact Report:
- Version change: 1.0.0 -> 2.0.0
- Modified principles:
  - "Separation of Concerns" -> REMOVED (replaced by new architecture)
  - "Type Safety" -> RETAINED (updated for new stack)
  - "Stateless Security" -> "Stateless AI" (redefined for AI context)
  - "Modern Standards" -> REMOVED (merged into Technology Standards)
- Added sections:
  - Agentic Workflow (new core principle)
  - Tool-First (new core principle)
  - Model Agnosticism (new core principle)
  - AI Provider Configuration (new section)
- Removed sections:
  - Security and Deployment Constraints (merged into constraints)
- Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending review for MCP/Agent alignment
  - .specify/templates/spec-template.md ⚠ pending review for MCP/Agent alignment
  - .specify/templates/tasks-template.md ⚠ pending review for MCP/Agent alignment
- Follow-up TODOs: None
-->

# Todo AI Chatbot Constitution

## Core Principles

### Agentic Workflow
AI operates via the OpenAI Agents SDK (configured for OpenRouter) using explicit MCP tools.
All AI interactions MUST be routed through the Agent framework; direct model calls are prohibited.
Tool invocations are the sole mechanism for AI-driven actions; no implicit behavior allowed.
Agent configuration MUST specify OpenRouter as the provider endpoint.

### Stateless AI
The server holds no conversation state in memory; all context is hydrated from the DB per request.
Each request MUST reconstruct conversation context from the `Conversation` and `Message` tables.
No in-memory caching of conversation state between requests.
Session continuity is achieved solely through database persistence, not server memory.

### Tool-First
All database modifications (CRUD) MUST happen via formal MCP Tools, not direct arbitrary SQL execution.
MCP Tools are the exclusive interface for data mutations: Add, List, Complete, Delete, Update.
Direct ORM calls outside of MCP tool handlers are prohibited for task operations.
Tool definitions MUST be registered with the MCP SDK and exposed to the Agent.

### Model Agnosticism
System MUST work with OpenRouter-compatible models (e.g., `anthropic/claude-3.5-sonnet`, `openai/gpt-4o`).
No model-specific code paths; all interactions use the unified OpenAI Agents SDK interface.
Model selection is a runtime configuration, not a code-level decision.
Provider-specific features MUST NOT be relied upon unless wrapped in an abstraction.

### Type Safety
Full typing in Python (Pydantic/SQLModel) and TypeScript.
All API contracts MUST be strongly typed; no implicit `Any` types in public interfaces.
MCP Tool input/output schemas MUST use Pydantic models for validation.
Type checking MUST pass in CI pipeline before merge.

## Technology Standards

**Stack:**
- Frontend: Next.js 16+ (App Router), OpenAI ChatKit
- Backend: FastAPI, OpenAI Agents SDK, Official MCP SDK (`mcp`)
- Database: SQLModel ORM with `Conversation` and `Message` tables, Neon Serverless Postgres

**AI Provider:**
- Provider: OpenRouter
- Base URL: `https://openrouter.ai/api/v1`
- Environment Variable: `OPENROUTER_API_KEY` (NOT `OPENAI_API_KEY`)

**Protocol:**
- Model Context Protocol (MCP) for all tool definitions
- RESTful API standards for non-AI endpoints

**Code Style:**
- Python: PEP 8
- TypeScript: ESLint/Prettier
- All database interactions via SQLModel ORM

## Constraints

**SDK Usage:**
- MUST use the Official MCP SDK (`mcp` package)
- MUST use OpenAI Agents SDK for agent orchestration
- No custom tool-calling implementations; use SDK primitives

**Persistence:**
- Chat history MUST be stored in Neon (Postgres)
- `Conversation` table: conversation metadata and user association
- `Message` table: individual messages with role, content, timestamps

**Security:**
- Agents can ONLY access tasks belonging to the authenticated `user_id`
- User context MUST be validated on every tool invocation
- No cross-user data access permitted

**Configuration:**
- `OPENROUTER_API_KEY` environment variable required
- Base URL configured to OpenRouter endpoint
- Model ID passed as runtime parameter

## Success Criteria

- User can manage tasks purely through natural language
- Backend successfully routes Agent requests via OpenRouter
- MCP Tools function correctly: Add, List, Complete, Delete, Update
- Conversation history persists across sessions
- Tool invocations respect user isolation

## Governance

This constitution governs all development activities for the Todo AI Chatbot.
All code reviews MUST verify compliance with these principles.
Deviations require explicit approval and documentation via ADR.
Changes to this constitution require team consensus and formal amendment process.

**Version**: 2.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-09
