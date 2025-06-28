# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JARVIS is a personal AI assistant with two main components:

1. **Voice Assistant** (`src/jarvis_livekit_agent.py`) - Real-time voice interaction using LiveKit
2. **Software Factory** (`src/SoftwareFactory/`) - Autonomous code generation system using LangGraph

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Activate virtual environment (if using venv)
source venv/bin/activate
```

### Running the Application
```bash
# Run the main JARVIS voice assistant
python src/jarvis_livekit_agent.py

# Run the software factory standalone
python src/SoftwareFactory/factory_main.py
```

### Code Quality
```bash
# Run linting
ruff check src/

# Run tests
pytest tests/
```

## Architecture

### Voice Assistant Architecture
- **Entry point**: `jarvis_livekit_agent.py:20` - `entrypoint()` function
- **Agent modes**: 
  - `MULTIMODAL` - Uses OpenAI Realtime API for audio+text
  - `VOICE` - Uses pipeline with separate STT/TTS/LLM components
- **Function calling**: Defined in `functions.py:16` - `Functions` class extends `llm.FunctionContext`
- **Smart home simulation**: Basic light control across 3 rooms (living room, bedroom, kitchen)

### Software Factory Architecture
The Software Factory is a **LangGraph state machine** that autonomously generates code projects:

**Core Components:**
- **State Management**: `company_state.py:14` - `CompanyState` tracks project requirements, plans, and messages
- **Agent Graph**: `factory_main.py:68` - `create_company_graph()` defines the workflow
- **Node Execution**: Three main nodes with specific responsibilities

**Workflow (Graph Nodes):**
1. **Planner Node** (`factory_main.py:39`) - Converts requirements into step-by-step plans
2. **Developer Node** (`factory_main.py:48`) - Executes the plan using file system tools
3. **Tester Node** (`factory_main.py:58`) - Tests generated code and provides feedback

**Agent Creation:**
- **Agents**: `chains.py:40` - `get_coder_agent()`, `get_tester_agent()` create ReAct agents
- **Prompts**: `prompthub.py` - Contains system prompts for each agent type
- **Tools**: `factory_tools.py` - File system operations (create/read/delete files/directories)

**Key Constraints:**
- All generated projects must be created in a `projects/` directory
- Agents assume environment variables are set in `~/.zshrc`
- Generated code must include a README.md with run instructions
- Tester agents use new terminal windows for server testing

### Tool System
The Software Factory uses **LangChain tools** for file operations:
- `create_directory`, `delete_directory`, `list_files_in_directory`
- `create_file_with_code`, `read_file`, `delete_file`
- `run_terminal_command`, `run_terminal_command_in_new_terminal`

### State Flow
1. **CompanyState** initialized with `project_requirements`
2. **Planner** creates step-by-step plan
3. **Developer** executes plan using file tools
4. **Tester** validates output and provides feedback
5. Loop continues until project is complete or max iterations reached

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - Required for all AI functionality
- `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` - Required for voice assistant

### Model Configuration
- Voice Assistant: Uses `gpt-4o-mini` by default
- Software Factory: Uses `gpt-4o-mini` with 16k max tokens

## Important Notes

- **Security**: Never commit API keys - they should be in environment variables only
- **Testing**: Tester agents automatically start servers in new terminals for API testing
- **Dependencies**: Project uses `uv` for dependency management (see `uv.lock`)
- **Voice Models**: Pre-trained TTS models available in `checkpoints_v2/` for multiple languages
- **Generated Projects**: All Software Factory output goes to `projects/` directory (not tracked in git)