# MZ (Monozukuri) - Personal AI Assistant

> 🤖 An evolving AI assistant inspired by Kokoro

## About

MZ is my long-term project to build a personal AI assistant that 
grows in capability over time. Starting as a simple conversational 
agent, MZ will eventually develop autonomous decision-making, 
ethical reasoning, and self-improvement capabilities.

**Current Version:** v0.1  
**Status:** ✅ Working  
**Started:** December 2025

## Why I'm Building This

I decided to build something ambitious—both as a learning tool and 
as a portfolio piece that demonstrates my ability to ship real 
projects.

MZ represents my commitment to:
- Learning by building 
- Long-term thinking
- Public development

## Current Capabilities (v0.1)

- 💬 Intelligent conversation using Claude API
- 🧠 Conversation memory within sessions
- 🔐 Secure API key management
- 📝 JSON-based persistent storage
- 🛡️ Error handling and self-healing memory
- 🏗️ Modular, maintainable codebase

## Tech Stack

- **Language:** Python 3.13
- **AI:** Claude (Anthropic API)
- **Storage:** JSON

## Setup

1. Clone the repository
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Create a `.env` file in the project root:
```
   ANTHROPIC_API_KEY=your_key_here
```
4. Run MZ:
```bash
   cd versions/v0.1
   python monozukuri.py
```

## Roadmap

See `docs/roadmap.md` for the complete development plan from v0.1 to 
v2.5.

**Next up (v0.2):** Task management and daily productivity features

## Project Structure
```
Monozukuri/
├── versions/          # Version-specific code
│   └── v0.1/         # Current version
├── data/             # Persistent storage
├── docs/             # Documentation and planning
├── research/         # Papers and inspiration
├── tests/            # Test suite (coming in v1.0)
└── sandbox/          # Experiments
```

## Learning Journey

This project is as much about my growth as a developer as it is 
about building MZ. Each version teaches new concepts:
- v0.1: API integration, memory systems, error handling
- v0.2: CRUD operations, command parsing (planned)
- v0.3: Code analysis, educational systems (planned)

## Philosophy

Inspired by Kokoro—an AI designed to make profound decisions about 
humanity's future. MZ's journey mirrors my own: starting with 
basics, gradually developing deeper reasoning capabilities, and 
ultimately becoming something genuinely useful.

## License

This is a personal learning project. Feel free to learn from it, but 
please don't copy it wholesale for commercial purposes.

---

*"The question isn't whether AI will change the world. It's whether 
we'll build AI that changes it for the better."*
