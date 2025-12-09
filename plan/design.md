# Guessme - System Design

AI-powered draw guessing game.

## Requirements

**Functional:** Single player, shareable game history via URL

**Non-functional:** Geo-distributed (24 regions), 99.99% availability, tolerates stroke loss

## Scale Estimation

| Metric | Value |
|--------|-------|
| DAU | 1M |
| Users/region | 40K |
| Games/user/day | 3 |
| Drawings/game | 5 |

**Data pipeline:**
```
Strokes (raw) → gzip (5x) → SVG → PNG 256×256 grayscale
  50KB      →   10KB    → 40KB →     8-15KB
```

**Storage:** 2-4 GB/day/region (after compression)

## Architecture

```
┌────────┐    WebSocket     ┌────────┐      ┌──────────┐      ┌──────────┐
│   FE   │ ←──(gzip)────→   │   BE   │ ───→ │ MQ (in)  │ ───→ │  Stream  │
│ Vue.js │                  │FastAPI │      └──────────┘      │ Processor│
└────────┘                  └────┬───┘                        └────┬─────┘
     ↑                          │                                  │
     │         "turtle"         │                                  ↓
     └──────────────────────────┤                            ┌──────────┐
                                │      ┌──────────┐          │ ML Model │
                                └───── │ MQ (out) │ ←────────└──────────┘
                                       └──────────┘   "turtle"
```

**Flow:** FE → strokes → BE → MQ(in) → Stream Processor → PNG → ML → prediction("turtle") → MQ(out) → BE → WS → FE

## Tech Stack

| Layer | Phase 1 | Phase 2 |
|-------|---------|---------|
| Frontend | Vue.js + Vite | - |
| Backend | FastAPI + uv | - |
| Message Queue | RabbitMQ | Kafka |
| Stream Processing | Ray | Flink |

**Note:** Abstract MQ/stream interfaces for phase migration.

## Testing

| Scope | Framework |
|-------|-----------|
| E2E | Playwright |
| Backend | pytest |
| Frontend | Vitest |

