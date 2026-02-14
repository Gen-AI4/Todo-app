---
id: 002
title: Create ChatKit Frontend Implementation Plan
stage: plan
date: 2026-02-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: 007-chatkit-frontend
branch: 007-chatkit-frontend
user: Adi
command: /sp.plan
labels: ["plan", "chatkit", "frontend", "nextjs", "tailwind"]
links:
  spec: specs/007-chatkit-frontend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/007-chatkit-frontend/plan.md
tests:
  - null
---

## Prompt

/sp.plan

Create: ChatPage component, ChatProvider configuration, Custom Fetcher for ChatKit.
Decisions needing documentation: Streaming response handling (if supported by OpenRouter/Backend) vs. Request/Response.
Testing strategy: End-to-end test - Type in UI, see it appear in DB, see AI response in UI.

Technical details:
- Phase 1: Install ChatKit package.
- Phase 2: Create a ChatInterface component.
- Phase 3: Implement a custom fetcher in ChatKit to direct requests to our FastAPI backend (instead of default OpenAI endpoints).
- Phase 4: Handle "Loading" states.

## Response snapshot

Created 4-phase implementation plan:

**Phase 1: Project Scaffold** - Recreate package.json (source files were lost), add @openai/chatkit, recreate config files, npm install
**Phase 2: Auth & API Layer** - better-auth client, custom fetch wrapper with JWT injection for POST /api/chat
**Phase 3: Chat Interface** - ChatInterface component with React state management, Tailwind-styled chat bubbles (user=right/blue, AI=left/gray), loading indicator, error handling, auto-scroll
**Phase 4: Page Integration** - Dashboard page with embedded chat, login/register pages, root redirect

**Key discovery:** Frontend source files were deleted (only node_modules and .next build artifacts remain). Recovered tech stack from build: Next.js 16, React 19, Tailwind CSS 4, better-auth, swr. Must recreate source from scratch.

**ADR decisions:**
- ADR-006: Request/response (non-streaming) for v1 - backend doesn't support streaming
- ADR-007: Custom state management over ChatKit provider - backend API shape differs from OpenAI format

**New files:** package.json, configs, layout.tsx, page.tsx, dashboard/page.tsx, login/page.tsx, register/page.tsx, components/ChatInterface.tsx, lib/auth.ts, lib/api.ts

## Outcome

- Impact: Complete implementation plan for ChatKit frontend integration
- Tests: E2E manual testing strategy defined
- Files: 1 file created (plan.md)
- Next prompts: /sp.tasks to generate task list, /sp.implement to execute
- Reflection: Frontend source loss means significant recreation effort; build artifacts provided enough info to reconstruct the tech stack
