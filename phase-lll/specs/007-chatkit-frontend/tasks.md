# Tasks: ChatKit Frontend Integration

**Input**: Design documents from `/specs/007-chatkit-frontend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: End-to-end manual testing - type in UI, see in DB, see AI response. No automated tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/app/`, `frontend/components/`, `frontend/lib/`
- Paths based on plan.md structure

---

## Phase 1: Setup (Project Scaffold)

**Purpose**: Recreate frontend project structure and install dependencies

- [x] T001 Create frontend/package.json with existing deps (next 16.1.6, react 19.2.3, tailwindcss 4, better-auth, swr, clsx, tailwind-merge) plus @openai/chatkit
- [x] T002 Create frontend/tsconfig.json with Next.js 16 App Router paths configuration (@/ alias)
- [x] T003 [P] Create frontend/next.config.ts with output: "standalone" and image config
- [x] T004 [P] Create frontend/postcss.config.mjs with @tailwindcss/postcss plugin
- [x] T005 Create frontend/app/globals.css with Tailwind CSS 4 @import "tailwindcss" and base styles
- [x] T006 Run npm install in frontend/ directory to install all dependencies

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Root layout, auth client, and API helper that MUST be complete before any user story

**CRITICAL**: No UI components can be built until this phase is complete

### Root Layout

- [x] T007 Create frontend/app/layout.tsx with html/body structure, globals.css import, metadata (title: "Todo AI Chatbot"), and children prop
- [x] T008 [P] Create frontend/app/page.tsx as root page that redirects to /dashboard or /login based on auth state

### Auth Client

- [x] T009 Create frontend/lib/auth.ts with better-auth createAuthClient configured with NEXT_PUBLIC_API_URL base URL

### Chat API Helper (FR-002, FR-003)

- [x] T010 Create frontend/lib/api.ts with sendChatMessage() function that POSTs to /api/chat with JWT Authorization header, message body, and optional conversation_id
- [x] T011 Add TypeScript types for ChatApiResponse (response: string, conversation_id: string) in frontend/lib/api.ts

**Checkpoint**: Foundation ready - layout renders, auth client configured, API helper typed

---

## Phase 3: User Story 1 - User Opens the Chat Interface (Priority: P1) MVP

**Goal**: User navigates to app and sees a chat interface with input field and send button

**Independent Test**: Load /dashboard in browser, verify chat interface is visible with input and send button

### Implementation for User Story 1

- [x] T012 [US1] Create frontend/components/ChatInterface.tsx with "use client" directive, empty component shell returning a container div
- [x] T013 [US1] Add text input field with placeholder "Type a message..." and controlled state in frontend/components/ChatInterface.tsx
- [x] T014 [US1] Add send button next to input field in frontend/components/ChatInterface.tsx
- [x] T015 [US1] Add welcome/placeholder text in the empty message area: "Hello! I can help you manage your tasks. Try saying 'Add a task called Buy milk'" in frontend/components/ChatInterface.tsx
- [x] T016 [US1] Disable send button when input is empty (FR-011) in frontend/components/ChatInterface.tsx
- [x] T017 [US1] Create frontend/app/dashboard/page.tsx that renders ChatInterface component with auth token from session
- [x] T018 [US1] Style the chat container as a full-height flex column with Tailwind in frontend/components/ChatInterface.tsx: messages area (flex-grow, overflow-y-auto) + input bar (flex-shrink-0) at bottom
- [x] T019 [US1] Verify in browser: /dashboard shows chat interface with input field and send button

**Checkpoint**: Chat interface visible and styled - user can see the input field

---

## Phase 4: User Story 2 - User Sends a Message and Receives a Response (Priority: P1)

**Goal**: User types message, sees it on the right as a blue bubble, AI response appears on the left as gray bubble

**Independent Test**: Type "Add a task called Buy milk", send, verify user bubble appears right, AI response appears left

### Implementation for User Story 2

- [x] T020 [US2] Add messages state array (role + content) to ChatInterface in frontend/components/ChatInterface.tsx
- [x] T021 [US2] Implement handleSend() in frontend/components/ChatInterface.tsx: add user message to state, call sendChatMessage(), add assistant response to state
- [x] T022 [US2] Store conversation_id from first response and pass it in subsequent requests in frontend/components/ChatInterface.tsx
- [x] T023 [US2] Render message list in the messages area: map over messages array in frontend/components/ChatInterface.tsx
- [x] T024 [US2] Style user messages: right-aligned (ml-auto), blue background (bg-blue-500 text-white), rounded bubble, max-width ~70% in frontend/components/ChatInterface.tsx
- [x] T025 [US2] Style AI messages: left-aligned (mr-auto), gray background (bg-gray-200 text-gray-900), rounded bubble, max-width ~70% in frontend/components/ChatInterface.tsx
- [x] T026 [US2] Add loading indicator: show pulsing dots or spinner below messages while waiting for response (FR-008) in frontend/components/ChatInterface.tsx
- [x] T027 [US2] Add Enter key handler to submit message on Enter press in frontend/components/ChatInterface.tsx
- [x] T028 [US2] Verify in browser: send "Hello", see user bubble right, AI response left, loading spinner appears during wait

**Checkpoint**: Core send/receive loop working with visual distinction

---

## Phase 5: User Story 3 - Multi-Message Conversation (Priority: P1)

**Goal**: Multiple messages persist in the chat, auto-scroll works, context maintained

**Independent Test**: Send 3+ messages, verify all visible, AI demonstrates context awareness

### Implementation for User Story 3

- [x] T029 [US3] Add auto-scroll to bottom on new messages using useRef and useEffect on messages array in frontend/components/ChatInterface.tsx
- [x] T030 [US3] Verify conversation_id is reused across all messages after first response in frontend/components/ChatInterface.tsx
- [x] T031 [US3] Verify in browser: send 3 messages, all visible with scroll, bot references earlier context

**Checkpoint**: Multi-turn conversations work with auto-scroll

---

## Phase 6: User Story 4 - Visual Distinction Between Participants (Priority: P2)

**Goal**: User and AI messages are immediately distinguishable via alignment, color, and style

**Independent Test**: View conversation, instantly identify who sent each message

### Implementation for User Story 4

- [x] T032 [US4] Add labels or avatars above message bubbles: "You" for user, "Assistant" for AI in frontend/components/ChatInterface.tsx
- [x] T033 [US4] Add subtle shadow or border to message bubbles for depth in frontend/components/ChatInterface.tsx
- [x] T034 [US4] Verify in browser: conversation with mixed messages has clear visual distinction

**Checkpoint**: Message authorship is instantly obvious

---

## Phase 7: User Story 5 - Graceful Error Handling (Priority: P2)

**Goal**: Backend errors show friendly message in chat, user can retry

**Independent Test**: Stop backend, send message, verify friendly error in chat, send again when backend restarts

### Implementation for User Story 5

- [x] T035 [US5] Add error state to ChatInterface that displays error message as a system message in the chat area in frontend/components/ChatInterface.tsx
- [x] T036 [US5] Handle fetch errors in handleSend(): catch network errors, display "Unable to reach the assistant. Please try again." in frontend/components/ChatInterface.tsx
- [x] T037 [US5] Handle non-200 HTTP responses in sendChatMessage(): throw descriptive error in frontend/lib/api.ts
- [x] T038 [US5] Ensure error state clears when user sends next message in frontend/components/ChatInterface.tsx
- [x] T039 [US5] Verify in browser: stop backend, send message, see friendly error, restart backend, send again successfully

**Checkpoint**: Error states handled gracefully without breaking the UI

---

## Phase 8: Auth Pages & Polish

**Purpose**: Login/register pages and cross-cutting concerns

### Auth Pages

- [x] T040 [P] Create frontend/app/login/page.tsx with email/password form, submit via authClient.signIn.email(), redirect to /dashboard on success
- [x] T041 [P] Create frontend/app/register/page.tsx with email/password/name form, submit via authClient.signUp.email(), redirect to /dashboard on success

### Polish & Cross-Cutting

- [x] T042 Make ChatInterface responsive for mobile (min 375px width): full-width messages, smaller padding on small screens in frontend/components/ChatInterface.tsx
- [x] T043 Add .env.local.example to frontend/ with NEXT_PUBLIC_API_URL placeholder
- [ ] T044 Verify full E2E flow: register -> login -> chat -> see tasks created in DB

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup (npm install) - BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational - establishes the chat UI shell
- **US2 (Phase 4)**: Depends on US1 - adds send/receive to the existing shell
- **US3 (Phase 5)**: Depends on US2 - extends with scroll and context
- **US4 (Phase 6)**: Depends on US2 - enhances existing message styling
- **US5 (Phase 7)**: Depends on US2 - wraps send logic with error handling
- **Auth Pages (Phase 8)**: Can start after Foundational (parallel to US1+)

### User Story Dependencies

| Story | Can Start After | Logical Prerequisites |
|-------|-----------------|----------------------|
| US1 (chat display) | Foundational | Layout and API helper ready |
| US2 (send/receive) | US1 | Input and container exist |
| US3 (multi-turn) | US2 | Send loop working |
| US4 (visual polish) | US2 | Messages rendering |
| US5 (error handling) | US2 | Send logic to wrap |

### Parallel Opportunities

- Setup: T003, T004 can run in parallel
- Foundational: T008 parallel with T009-T011
- Auth pages: T040, T041 run in parallel
- US4 and US5 can run in parallel after US2

---

## Implementation Strategy

### MVP First (US1 + US2)

1. Complete Phase 1: Setup + npm install
2. Complete Phase 2: Foundational (layout, auth, API helper)
3. Complete Phase 3: US1 (chat interface visible)
4. Complete Phase 4: US2 (send/receive working)
5. **STOP and VALIDATE**: Can user chat with AI?
6. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational -> Framework ready
2. US1 -> Chat visible -> Testable
3. US2 -> Send/receive -> MVP!
4. US3 -> Multi-turn -> Enhanced
5. US4 + US5 (parallel) -> Polished
6. Auth Pages -> Complete app

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 44 |
| Setup Tasks | 6 |
| Foundational Tasks | 5 |
| US1 (chat display) Tasks | 8 |
| US2 (send/receive) Tasks | 9 |
| US3 (multi-turn) Tasks | 3 |
| US4 (visual polish) Tasks | 3 |
| US5 (error handling) Tasks | 5 |
| Auth + Polish Tasks | 5 |
| Parallel Opportunities | 6 tasks marked [P] |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Frontend source was lost - all files are created fresh
- Testing is E2E manual (no automated tests)
- ChatKit may be used for visual components; state managed manually via React hooks
- If ChatKit components don't fit custom API shape, fall back to plain Tailwind chat bubbles
