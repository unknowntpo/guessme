# Epic: Frontend with Mock Server

**Status:** Done

## Summary

Vue 3 drawing game frontend with mock WebSocket server for fake ML predictions.

## What Was Built

### Frontend (`frontend/`)
- **Stack:** Vue 3 + Vite + TypeScript + Tailwind CSS
- **Components:** Timer, DrawingCanvas, PredictionsList, FinalResult, GameControls
- **Composables:** useTimer, useCanvas, useGame
- **Services:** WebSocket client with ULID clientId (localStorage)
- **Tests:** 50 unit tests (Vitest)

### Mock Server (`mock-server/`)
- WebSocket server returning fake ML predictions
- Streams predictions every 500ms while drawing

### CI (`.github/workflows/`)
- GitHub Actions: test + build on push/PR

---

## Refactoring: Style Guide to Tailwind CSS

**Status:** Done

Converted `plan/style-guide.md` from pure CSS to Tailwind CSS equivalents.

### Checklist
- [x] Color palette → Tailwind `bg-*`, `text-*` classes
- [x] Typography → `font-mono`, `font-sans` classes
- [x] Buttons → Document `.btn` utility + Tailwind equivalent
- [x] Cards → `shadow-offset-*` classes
- [x] Badges/Tags → Tailwind classes
- [x] List Items → Tailwind classes
- [x] Progress Bars → Tailwind classes
- [x] Layout/Container → `max-w-[1302px] mx-auto px-6`
- [x] Animations → Keep CSS keyframes, document usage
- [x] Mobile/Responsive → Keep `@media (hover: hover)` pattern
- [x] Quick Reference table → CSS → Tailwind mapping
- [x] Example Components → Tailwind class versions
