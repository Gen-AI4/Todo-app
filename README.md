# Multi-Phase AI-Native Todo Application Evolution

This project demonstrates the evolution of a Todo application through various levels of complexity, following a Spec-Driven Development (SDD) workflow.

## Project Structure

The application is developed in phases, each located in its own directory:

- **phase-l/**: In-Memory Python Console App. Focuses on core business logic and clean architecture.
- **phase-ll/**: Full-Stack Web Application. Introduces FastAPI (Backend), Next.js (Frontend), and PostgreSQL (Persistence).
- **phase-lll/**: AI-Native Evolution. Integrates AI agents and advanced organizational features.

## Development Workflow (SDD)

This project strictly adheres to Spec-Driven Development principles:

1. **Specifications**: Located in `specs/`. Every feature starts with a `spec.md`.
2. **Planning**: Architecture and technical decisions are documented in `plan.md` within each feature folder.
3. **Execution**: Actionable tasks are defined in `tasks.md` and tracked as they are implemented.
4. **History**: A full record of AI interactions is maintained in `history/prompts/` for traceability and learning.

## Getting Started

Refer to the README files within each phase directory for specific setup and execution instructions:

- [Phase I README](./phase-l/README.md)
- [Phase II README](./phase-ll/Todo-App/README.md)
- [Phase III README](./phase-lll/Todo-App/README.md)

## Constitution

The project is governed by a central [Constitution](./.specify/memory/constitution.md) that defines core principles, technology stacks, and quality standards for all phases.
