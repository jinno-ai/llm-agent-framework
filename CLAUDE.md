# Claude Code Instructions for LLM Agent Framework

## Quick Start for Claude Code

This repository is a **multi-agent orchestration system** built with LangGraph. When working with this codebase:

### Primary Commands
```bash
# Run tests
pytest tests/ -v

# Run specific tests
pytest tests/test_react_agent.py -v

# Start development
python run.py dev

# Run linter
ruff check agent_framework/

# Type checking
mypy agent_framework/
```

### Key Files to Understand
- `agent_framework/agents/` - Core agent implementations
- `agent_framework/tools/` - Tool integrations
- `run.py` - Main entry point
- `tests/` - Test suite

## Development Workflow

### When Making Changes
1. **Read existing code** - Follow established patterns
2. **Write tests first** - Test-driven development approach
3. **Implement feature** - Keep changes minimal and focused
4. **Run linter/type checker** - Ensure code quality
5. **Test thoroughly** - Verify all tests pass
6. **Commit changes** - Use descriptive commit messages

### Code Style
- **Python 3.10+** with type hints
- **LangGraph patterns** for state machines
- **Async/await** for I/O operations
- **Error handling** with proper fallbacks
- **Logging** with structured format

## Architecture Overview

### Agent System
```
User Request → Supervisor Agent → Specialized Agents → Tools → Results
```

### Key Components
1. **BaseAgent**: Foundation for all agents
2. **ReActAgent**: Reasoning + Acting pattern
3. **SupervisorAgent**: Multi-agent coordination
4. **Tools**: Extensible tool ecosystem

### Memory System
- **Short-term**: Conversation buffer (Redis)
- **Long-term**: Vector memory (Pinecone)
- **Episodic**: Task history (PostgreSQL)

## Testing Strategy

### Unit Tests
```bash
pytest tests/unit/ -v --cov=agent_framework
```

### Integration Tests
```bash
pytest tests/integration/ -v
```

### Coverage Requirements
- Minimum: 80%
- Target: 90%

## Common Tasks

### Adding a New Agent
1. Create class inheriting from `BaseAgent`
2. Implement `execute()` method
3. Add tools via `self.tools`
4. Write comprehensive tests
5. Update documentation

### Adding a New Tool
1. Create class inheriting from `BaseTool`
2. Implement `execute()` method
3. Add input validation
4. Write tests with edge cases
5. Register in tool registry

### Debugging Agent Behavior
1. Enable LangSmith tracing
2. Check logs in `logs/` directory
3. Use `run.py debug` mode
4. Review agent state transitions
5. Monitor tool usage

## Performance Considerations

### Optimization Targets
- **Response Time**: < 5s per task
- **Success Rate**: > 90%
- **Tool Efficiency**: > 80%
- **Memory Usage**: < 500MB per agent

### Bottlenecks to Watch
- LLM API call latency
- Tool execution time
- Memory retrieval speed
- State synchronization

## Safety & Security

### Code Execution
- All code execution in sandboxed environments
- Resource limits enforced
- Timeout mechanisms in place
- No file system access without explicit permission

### API Usage
- Rate limiting implemented
- Cost tracking enabled
- Error handling with retries
- Fallback strategies defined

## Project Status

### Current Phase
**Phase 1: Core Agent Implementation** (Week 1-3)
- ✅ Base agent framework
- ✅ ReAct agent implementation
- 🚧 Specialized agents (Research, Coding, Data, Writing)
- 📋 Tool ecosystem expansion

### Next Steps
1. Complete specialized agents
2. Implement multi-agent collaboration
3. Add advanced memory systems
4. Build monitoring and debugging tools

## Troubleshooting

### Common Issues

**Agent not responding**
- Check LLM API credentials
- Verify rate limits not exceeded
- Review agent logs for errors

**Tool execution failures**
- Validate tool inputs
- Check external service availability
- Review error handling logic

**Memory issues**
- Clear conversation history
- Check Redis connection
- Verify vector database status

### Getting Help
1. Check `IMPLEMENTATION_ROADMAP.md` for architecture decisions
2. Review test files for usage examples
3. Examine logs in `logs/` directory
4. Use LangSmith for tracing agent behavior

---

**Repository**: llm-agent-framework
**Language**: Python 3.10+
**Framework**: LangGraph + LangChain
**Status**: Active Development