#!/usr/bin/env python3
"""
CLI Tool for LLM Agent Framework

Usage:
    python run.py single "Task description"
    python run.py multi "Complex task requiring multiple agents"
    python run.py interactive
    python run.py demo
"""

import argparse
import sys

from agent_framework.agents.supervisor import SupervisorAgent
from agent_framework.agents.react_agent import ReActAgent
from agent_framework.agents.base_agent import BaseAgent


class MockLLM:
    """Mock LLM for testing without API keys"""

    def __init__(self):
        self.call_count = 0

    def generate(self, prompt: str) -> str:
        """Generate mock response"""
        self.call_count += 1

        # Check if this is a ReAct agent prompt
        if "Question:" in prompt and "Thought:" in prompt and "Action:" in prompt:
            task = prompt.split("Question:")[-1].split("\n")[0].strip().lower()

            # Check if we already have some iterations (this is a continuation)
            if "Observation:" in prompt:
                # Extract the observation result
                observation_lines = [line for line in prompt.split("\n") if "Observation:" in line]
                if observation_lines:
                    last_observation = observation_lines[-1].split("Observation:")[-1].strip()

                    # This is a continuation, check if we should finish
                    if "search" in prompt.lower() or "calculator" in prompt.lower():
                        # We've used tools, now provide final answer
                        if "calculate" in task or "math" in task or "+" in task:
                            return f"Thought: I now know the final answer\nFinal Answer: The calculation result is {last_observation}"
                        else:
                            return f"Thought: I now know the final answer\nFinal Answer: Based on my research, here's what I found: {last_observation}"
                    else:
                        return f"Thought: I now know the final answer\nFinal Answer: Task completed successfully"
                else:
                    return f"Thought: I now know the final answer\nFinal Answer: Task completed successfully"
            else:
                # First iteration - decide what to do
                if "calculate" in task or "math" in task or "+" in task:
                    # Extract the actual math expression from the task
                    expression = task
                    return f"Thought: I need to calculate this mathematical expression\nAction: calculator\nAction Input: {expression}"
                elif "search" in task or "research" in task or "find" in task:
                    return f"Thought: I need to search for information\nAction: search\nAction Input: {task}"
                else:
                    return f"Thought: I should search for information about this\nAction: search\nAction Input: {task}"

        # Check if this is a supervisor planning prompt
        if "PLAN:" in prompt or "supervisor" in prompt.lower():
            if "research" in prompt.lower() and "code" in prompt.lower():
                return """PLAN:
Step 1: researcher - Research the latest AI trends and gather information
Step 2: coder - Create code to visualize the AI trends
COMPLETE: Task completed successfully with research and code."""
            elif "research" in prompt.lower():
                return """PLAN:
Step 1: researcher - Research the requested topic and gather comprehensive information
COMPLETE: Research completed."""
            else:
                return """PLAN:
Step 1: coder - Analyze the request and provide a solution
COMPLETE: Task completed."""

        # Simple pattern matching for single agent
        if "research" in prompt.lower():
            return "FINAL ANSWER: Based on research, I found relevant information about the topic."
        elif "code" in prompt.lower() or "python" in prompt.lower():
            return "FINAL ANSWER: Here's the code solution:\n\ndef solution():\n    return 'Hello World'"
        elif "analyze" in prompt.lower():
            return "FINAL ANSWER: Analysis complete. Key findings show positive trends."
        else:
            return "FINAL ANSWER: Task completed successfully."


def create_mock_tools():
    """Create mock tools for testing"""
    from agent_framework.tools.base_tool import SearchTool, CalculatorTool, PythonREPLTool

    return {
        "search": SearchTool(),
        "calculator": CalculatorTool(),
        "python_repl": PythonREPLTool()
    }


def single_agent_command(args):
    """Run single ReAct agent"""
    print("🤖 Initializing Single Agent Mode")
    print("=" * 60)

    # Create mock LLM
    llm = MockLLM()
    tools = create_mock_tools()

    # Create agent
    agent = ReActAgent(
        name="assistant",
        description="Helpful AI assistant",
        llm=llm,
        tools=tools,
        max_iterations=args.max_iterations
    )

    print(f"\n📝 Task: {args.task}")
    print(f"🔧 Available Tools: {', '.join(tools.keys())}")
    print("\n⏳ Running agent...\n")

    # Run agent
    result = agent.run(args.task)

    print("\n" + "=" * 60)
    print("✅ Result")
    print("=" * 60)
    print(f"\n{result}")
    print(f"\n📊 LLM Calls: {llm.call_count}")
    print(f"💾 Memory Entries: {len(agent.memory)}")


def multi_agent_command(args):
    """Run multi-agent system"""
    print("🤖 Initializing Multi-Agent System")
    print("=" * 60)

    # Create mock LLM
    llm = MockLLM()
    tools = create_mock_tools()

    # Create supervisor
    supervisor = SupervisorAgent(llm=llm, max_iterations=args.max_iterations)

    # Create specialized agents
    research_agent = ReActAgent(
        name="researcher",
        description="Researches information and gathers data",
        llm=llm,
        tools=tools
    )

    code_agent = ReActAgent(
        name="coder",
        description="Writes and reviews code",
        llm=llm,
        tools=tools
    )

    analyst_agent = ReActAgent(
        name="analyst",
        description="Analyzes data and provides insights",
        llm=llm,
        tools=tools
    )

    # Register agents
    supervisor.register_agent(research_agent)
    supervisor.register_agent(code_agent)
    supervisor.register_agent(analyst_agent)

    print(f"\n📝 Task: {args.task}")
    print(f"👥 Agents: {', '.join(supervisor.list_agents())}")
    print("\n⏳ Running multi-agent system...\n")

    # Run supervisor
    result = supervisor.run(args.task)

    print("\n" + "=" * 60)
    print("✅ Final Result")
    print("=" * 60)

    if result.get('success'):
        print(f"\n💡 Answer: {result['answer']}")
        print(f"\n📊 Iterations: {result.get('iterations', 'N/A')}")
        print(f"📋 Results from {len(result.get('results', []))} agent operations")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")


def interactive_command(args):
    """Interactive agent mode"""
    print("🤖 Interactive Agent Mode")
    print("=" * 60)
    print("Commands: single, multi, tools, quit\n")

    llm = MockLLM()
    tools = create_mock_tools()

    # Create agents
    single_agent = ReActAgent(
        name="assistant",
        description="Helpful assistant",
        llm=llm,
        tools=tools
    )

    supervisor = SupervisorAgent(llm=llm)
    for name in ["researcher", "coder", "analyst"]:
        agent = ReActAgent(
            name=name,
            description=f"{name} agent",
            llm=llm,
            tools=tools
        )
        supervisor.register_agent(agent)

    while True:
        try:
            cmd = input("🔧 Enter mode (single/multi/tools/quit): ").strip().lower()

            if cmd in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            elif cmd == 'single':
                task = input("📝 Enter task: ")
                result = single_agent.run(task)
                print(f"\n✅ {result}\n")

            elif cmd == 'multi':
                task = input("📝 Enter task: ")
                result = supervisor.run(task)
                if result.get('success'):
                    print(f"\n✅ {result['answer']}\n")
                else:
                    print(f"\n❌ {result.get('error')}\n")

            elif cmd == 'tools':
                print("\n🔧 Available Tools:")
                for name, tool in tools.items():
                    print(f"   • {name}: {tool.description}")

            else:
                print("⚠️  Unknown command")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def demo_command(args):
    """Run demonstration"""
    print("\n" + "=" * 60)
    print("🎭 Agent Framework Demo")
    print("=" * 60)

    llm = MockLLM()
    tools = create_mock_tools()

    # Demo 1: Single Agent
    print("\n📌 Demo 1: Single ReAct Agent")
    print("-" * 60)

    agent = ReActAgent(
        name="demo_agent",
        description="Demo agent",
        llm=llm,
        tools=tools
    )

    task = "What is 2 + 2?"
    print(f"Task: {task}")
    result = agent.run(task)
    print(f"Result: {result}")

    # Demo 2: Multi-Agent
    print("\n📌 Demo 2: Multi-Agent System")
    print("-" * 60)

    supervisor = SupervisorAgent(llm=llm)

    researcher = ReActAgent(name="researcher", description="Researcher", llm=llm, tools=tools)
    coder = ReActAgent(name="coder", description="Coder", llm=llm, tools=tools)

    supervisor.register_agent(researcher)
    supervisor.register_agent(coder)

    task = "Research AI trends and create code to visualize them"
    print(f"Task: {task}")

    result = supervisor.run(task)
    if result.get('success'):
        print(f"Result: {result['answer'][:100]}...")

    # Demo 3: Tool Usage
    print("\n📌 Demo 3: Tool Execution")
    print("-" * 60)

    for tool_name, tool in tools.items():
        print(f"\n• {tool_name}: {tool.description}")
        if tool_name == "calculator":
            print(f"  Test: 2 + 2 = {tool.run('2+2')}")
        elif tool_name == "search":
            print(f"  Test: {tool.run('Python')}")
        elif tool_name == "python_repl":
            print(f"  Test: {tool.run('print(\"Hello from Python!\")')}")

    print("\n" + "=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="LLM Agent Framework CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py single "Calculate 2 + 2"
  python run.py multi "Research AI and write code"
  python run.py demo
  python run.py interactive
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Single agent command
    single_parser = subparsers.add_parser('single', help='Run single agent')
    single_parser.add_argument('task', help='Task for the agent')
    single_parser.add_argument('--max-iterations', type=int, default=10,
                              help='Maximum iterations')

    # Multi-agent command
    multi_parser = subparsers.add_parser('multi', help='Run multi-agent system')
    multi_parser.add_argument('task', help='Complex task')
    multi_parser.add_argument('--max-iterations', type=int, default=10,
                              help='Maximum iterations')

    # Interactive command
    subparsers.add_parser('interactive', help='Interactive mode')

    # Demo command
    subparsers.add_parser('demo', help='Run demonstration')

    args = parser.parse_args()

    if args.command == 'single':
        single_agent_command(args)
    elif args.command == 'multi':
        multi_agent_command(args)
    elif args.command == 'interactive':
        interactive_command(args)
    elif args.command == 'demo':
        demo_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
