---
id: 002
title: Update Constitution for AI Chatbot Architecture
stage: constitution
date: 2026-02-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 003-frontend-app-logic
user: Adi
command: /sp.constitution
labels: ["constitution", "ai-chatbot", "mcp", "openrouter", "agents-sdk"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

Update

Project: Todo AI Chatbot (Next.js + FastAPI + Neon + MCP + OpenRouter)

Core principles:
- **Agentic Workflow:** AI operates via the OpenAI Agents SDK (configured for OpenRouter) using explicit MCP tools.
- **Stateless AI:** The server holds no conversation state in memory; all context is hydrated from the DB per request.
- **Tool-First:** All database modifications (CRUD) must happen via formal MCP Tools, not direct arbitrary SQL execution.
- **Model Agnosticism:** System must work with OpenRouter-compatible models (e.g., `anthropic/claude-3.5-sonnet` or `openai/gpt-4o`).

## Response snapshot

Updated constitution from v1.0.0 to v2.0.0 (MAJOR version bump). Added Agentic Workflow, Stateless AI, Tool-First, Model Agnosticism principles. Retained Type Safety. Added Technology Standards and Constraints sections.

## Outcome

- Impact: Major architectural shift from generic full-stack to AI-first chatbot paradigm
- Tests: No automated tests (governance document)
- Files: 1 file modified (.specify/memory/constitution.md)
- Next prompts: Review templates for MCP alignment; create ADR for architecture decision
- Reflection: Clean pivot from v1 to v2; principles are now testable and specific to AI/MCP workflow
