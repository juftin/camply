# STYLE_GUIDE: Coding & Git Standards

This document defines the engineering standards for `camply`. All agents and contributors MUST adhere to these rules to ensure a maintainable and consistent codebase.

---

## 🐍 Python Standards (Backend)

1.  **Strict Typing**: Every function signature MUST have type hints. Use `mypy` to verify.
2.  **Pydantic v2**: Use Pydantic for all data validation and DTOs. Prefer `BaseModel` and avoid raw dictionaries.
3.  **Async-First**: All I/O operations (DB queries, API calls) MUST be `async`.
4.  **Logging**: Use `structlog` for structured, JSON-compatible logging. Never use `print()`.
5.  **Docstrings**: Follow the **NumPy** docstring convention for all public methods and classes.

---

## ⚛️ React & TypeScript Standards (Frontend)

1.  **Functional Components**: Use arrow functions for components (`export const MyComponent = () => ...`).
2.  **TypeScript**: Avoid `any`. Define strict interfaces/types for all component props and state.
3.  **Tailwind CSS**: Use Tailwind classes for styling. Follow the standard utility order (Layout -> Box Model -> Typography -> Visuals).
4.  **Shadcn/UI**: Use Shadcn primitives for UI atoms. Do not modify the primitives in `src/components/ui/` directly; wrap them if needed.
5.  **TanStack Query**: Use React Query for all server-state. Keep API logic inside `src/lib/api.ts` or the generated SDK.

---

## 🌳 Git & PR Standards

1.  **Gitmoji**: Every commit message MUST start with a relevant [Gitmoji](https://gitmoji.dev/).
    - ✨ `:sparkles:` for new features.
    - 🐛 `:bug:` for bug fixes.
    - 📝 `:memo:` for documentation.
    - 🧪 `:test_tube:` for tests.
    - 🎨 `:art:` for UI/style changes.
2.  **Commit Messages**: Follow the "Why, not what" rule.
    - *Bad*: `✨ add unique_target model`
    - *Good*: `✨ Implement UniqueTarget model to support scan de-duplication`
3.  **Branching**: Work in isolated branches (or worktrees). Never commit directly to `main`.
4.  **PR Descriptions**: Every PR must include:
    - A summary of changes.
    - A link to the relevant `spec-kit` plan.
    - A screenshot or DB query result proving validation.

---

## 🧪 Testing Discipline

1.  **Coverage**: Every new feature MUST have corresponding tests.
2.  **VCR**: External API interactions MUST be recorded using `pytest-vcr`.
3.  **Red-Green-Refactor**: For bug fixes, write a failing test first to reproduce the issue.
