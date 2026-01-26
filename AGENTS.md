# AI Agent Development Guide

## Overview
This document guides AI agents (like Claude Code) on how to effectively work with the llm-agent-framework repository.

## Repository Purpose
Production-ready multi-agent orchestration system for complex task automation using LangGraph and modern LLM architectures.

## Key Architecture Components

### Agent Types
- **ReAct Agent**: Thought → Action → Observation loops
- **Reflection Agent**: Self-critique and output refinement
- **Specialized Agents**: Research, Coding, Data Analysis, Writing

### Core Technologies
- **LangGraph**: State machine management and workflow orchestration
- **LangChain**: Agent base and tool integration
- **AutoGen**: Conversational multi-agent systems
- **CrewAI**: Role-based agent collaboration

## Development Guidelines

### Code Structure
```
agent_framework/
├── agents/          # Agent implementations
│   ├── base_agent.py
│   ├── react_agent.py
│   └── supervisor.py
├── tools/           # Tool integrations
│   ├── base_tool.py
│   ├── code_tools.py
│   └── web_tools.py
├── memory/          # Memory systems
│   └── conversation_memory.py
└── utils/           # Utilities
```

### When Adding Features
1. **Test-Driven Approach**: Always add tests first
2. **Agent Patterns**: Follow ReAct, Reflection, or Plan & Solve patterns
3. **Tool Integration**: Use base_tool.py for consistency
4. **Memory Management**: Implement proper memory cleanup
5. **Error Handling**: Graceful degradation with fallback strategies

### Testing Strategy
- **Unit Tests**: `pytest tests/unit/ -v --cov`
- **Integration Tests**: `pytest tests/integration/ -v`
- **Agent Benchmarks**: Test multi-step task completion

### Common Commands
```bash
# Run development server
python run.py dev

# Run tests
pytest tests/ -v

# Run specific agent test
python tests/test_react_agent.py

# Start interactive mode
python run.py interactive
```

## AI-Specific Instructions

### For Code Generation
1. Follow existing code patterns in `agent_framework/`
2. Use type hints consistently
3. Add docstrings to all classes and functions
4. Ensure backward compatibility

### For Debugging
1. Check logs in `logs/` directory
2. Use LangSmith for tracing
3. Review agent state transitions
4. Monitor tool usage and performance

### For Documentation
1. Update README.md for user-facing changes
2. Update IMPLEMENTATION_ROADMAP.md for progress tracking
3. Add inline documentation for complex logic

## Important Constraints

### Performance Requirements
- Task success rate: > 90%
- Average response time: < 5s
- Tool usage efficiency: > 80%

### Code Quality
- Maximum cyclomatic complexity: 10
- Minimum test coverage: 80%
- All code must pass linting and type checking

### Architecture Principles
- Modularity: Agents should be independently testable
- Extensibility: Easy to add new tools and agents
- Observability: Built-in monitoring and debugging
- Safety: Sandboxed code execution and API limits

## Current Implementation Status

### Completed ✅
- Base agent framework
- ReAct agent implementation
- Basic tool integrations
- Conversation memory

### In Progress 🚧
- Multi-agent collaboration
- Advanced tool ecosystem
- Long-term memory system

### Planned 📋
- Self-improvement mechanisms
- Enterprise features
- Advanced monitoring

## Collaboration Notes

### Working with Multiple Agents
- Use SupervisorAgent for task delegation
- Implement proper message passing protocols
- Handle conflict resolution strategies
- Share context through shared memory

### Tool Development
- Extend BaseTool for new tools
- Implement proper error handling
- Add input validation
- Document tool usage and parameters

---

**Last Updated**: 2026-01-27
**Framework Version**: 1.0.0