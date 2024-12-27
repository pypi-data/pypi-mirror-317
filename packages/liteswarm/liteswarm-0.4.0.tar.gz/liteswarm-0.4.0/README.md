# LiteSwarm

LiteSwarm is a lightweight, extensible framework for building AI agent systems. It provides a minimal yet powerful foundation for creating both simple chatbots and complex agent teams, with customization possible at every level.

The framework is LLM-agnostic and supports 100+ language models through [litellm](https://github.com/BerriAI/litellm), including:
- OpenAI
- Anthropic (Claude)
- Google (Gemini)
- Azure OpenAI
- AWS Bedrock
- And many more

## Quick Navigation
- [Installation](#installation)
- [Requirements](#requirements)
- [Key Features](#key-features)
- [Core Components](#core-components)
- [Basic Usage](#basic-usage)
- [Event Streaming](#event-streaming)
- [Advanced Features](#advanced-features)
- [Key Concepts](#key-concepts)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

Choose your preferred installation method:

Using pip:
```bash
pip install liteswarm
```

Using uv (recommended for faster installation):
```bash
uv pip install liteswarm
```

Using poetry:
```bash
poetry add liteswarm
```

Using pipx (for CLI tools):
```bash
pipx install liteswarm
```

## Requirements

- Python 3.11 or higher
- Async support (asyncio)
- A valid API key for your chosen LLM provider

### API Keys
You can provide your API key in two ways:
1. Through environment variables:
   ```bash
   # For OpenAI
   export OPENAI_API_KEY=sk-...
   # For Anthropic
   export ANTHROPIC_API_KEY=sk-ant-...
   # For Google
   export GOOGLE_API_KEY=...
   ```

   or using os.environ:
   ```python
   import os

   # For OpenAI
   os.environ["OPENAI_API_KEY"] = "sk-..."
   # For Anthropic
   os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."
   # For Google
   os.environ["GOOGLE_API_KEY"] = "..."
   ```

2. Using a `.env` file:
   ```env
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=...
   ```

3. Using the `LLM` class:
   ```python
   from liteswarm.types import LLM

   llm = LLM(
       model="gpt-4o",
       api_key="sk-...", # or api_base, api_version, etc.
   )
   ```

See [litellm's documentation](https://docs.litellm.ai/docs/providers) for a complete list of supported providers and their environment variables.

## Key Features

- **Lightweight Core**: Minimal base implementation that's easy to understand and extend
- **LLM Agnostic**: Support for 100+ language models through litellm
- **Flexible Agent System**: Create agents with custom instructions and capabilities
- **Tool Integration**: Easy integration of Python functions as agent tools
- **Structured Outputs**: Built-in support for validating and parsing agent responses
- **Multi-Agent Teams**: Coordinate multiple specialized agents for complex tasks
- **Event Streaming**: Real-time streaming of agent responses, tool calls, and other events
- **Context Management**: Smart handling of conversation history and context
- **Cost Tracking**: Optional tracking of token usage and API costs

## Core Components

### Message Store

The Message Store is responsible for managing conversation history and message persistence. It provides:

- **Message Storage**: Efficient storage and retrieval of conversation messages
- **History Management**: Methods for adding, updating, and removing messages
- **State Preservation**: Maintains conversation state between interactions
- **Memory Optimization**: Support for different memory strategies
- **Format Validation**: Ensures messages follow the required schema

Example usage:
```python
import asyncio

from liteswarm.core.message_store import LiteMessageStore
from liteswarm.types import Message


async def main() -> None:
    # Create a message store
    message_store = LiteMessageStore()

    # Add messages to the message store
    await message_store.add_messages(
        [
            Message(role="user", content="Hello!"),
            Message(role="assistant", content="Hello! How can I help you today?"),
        ]
    )

    # Get all messages in the message store
    messages = await message_store.get_messages()

    # Display results
    print("Messages:")
    for message in messages:
        print(f"- {message.content}")


if __name__ == "__main__":
    asyncio.run(main())
```

See [MessageStore](liteswarm/core/message_store.py) for more details.

### Message Index

The Message Index provides semantic search capabilities over conversation history:

- **Semantic Search**: Find messages based on meaning, not just keywords
- **Relevance Scoring**: Rank messages by semantic similarity
- **Embedding Support**: Multiple embedding models (OpenAI, HuggingFace, etc.)
- **Efficient Retrieval**: Fast lookup of relevant context
- **Customizable Search**: Configurable search parameters and strategies

Example usage:
```python
import asyncio

from liteswarm.core import LiteMessageIndex
from liteswarm.types import Message, MessageRecord


async def main() -> None:
    # Create an index
    index = LiteMessageIndex()

    # Prepare chat messages for indexing
    # fmt: off
    messages = [
        Message(role="user", content="Can you help me with setting up a development environment?"),
        Message(role="assistant", content="Sure! What kind of development environment are you working on?"),
        Message(role="user", content="I want to set up a Flutter development environment."),
        Message(role="assistant", content="To set up Flutter, you’ll need to install Flutter SDK, an IDE like VS Code or Android Studio, and ensure you have the required tools for your platform."),
        Message(role="user", content="What are the system requirements for running Flutter?"),
        Message(role="assistant", content="The system requirements depend on your operating system. For example, on macOS, you need macOS 10.14 or later and Xcode installed."),
    ]
    # fmt: on

    # Convert messages to MessageRecord
    chat_messages = [MessageRecord.from_message(message) for message in messages]

    # Add messages to index
    await index.index(chat_messages)

    # Find relevant messages
    relevant_messages = await index.search(
        query="system requirements for Flutter",
        max_results=10,
        score_threshold=0.6,
    )

    # Display the results
    print("Relevant messages:")
    for message, score in relevant_messages:
        print(f"- {message.content} (score: {score:.2f})")


if __name__ == "__main__":
    asyncio.run(main())
```

See [MessageIndex](liteswarm/core/message_index.py) for more details.

### Context Manager

The Context Manager optimizes conversation context to prevent token limits and improve relevance:

- **Context Optimization**: Smart selection of relevant messages
- **Window Management**: Sliding window over conversation history
- **RAG Integration**: Retrieval-augmented generation support
- **Strategy Selection**: Multiple optimization strategies
- **Token Management**: Automatic handling of context length

Example usage:
```python
import asyncio

from liteswarm.core import LiteContextManager, LiteMessageStore
from liteswarm.types import Message
from liteswarm.types.context_manager import RAGStrategyConfig


async def main() -> None:
    # Create message store that the context manager will use
    message_store = LiteMessageStore()

    # Add messages to the message store
    # fmt: off
    await message_store.add_messages(
        [
            Message(role="user", content="Hi there!"),
            Message(role="assistant", content="Hello! How can I assist you today?"),
            Message(role="user", content="Can you tell me the weather in London?"),
            Message(role="assistant", content="Sure! The weather in London is currently sunny with a high of 20°C."),
            Message(role="user", content="Thanks! How about Paris?"),
            Message(role="assistant", content="You're welcome! The weather in Paris is cloudy with occasional rain showers and a high of 15°C."),
            Message(role="user", content="What should I pack for a trip to both cities?"),
            Message(role="assistant", content="For London, pack light layers and sunglasses. For Paris, consider bringing an umbrella and a warm jacket."),
            Message(role="user", content="Got it. What are some must-see attractions in both cities?"),
            Message(role="assistant", content="In London, visit the Tower of London and Buckingham Palace. In Paris, don't miss the Eiffel Tower and the Louvre Museum."),
        ]
    )
    # fmt: on

    # Create context manager
    context_manager = LiteContextManager(message_store=message_store)

    # Optimize context using RAG strategy
    optimized_context = await context_manager.optimize_context(
        model="gpt-4o",
        strategy="rag",
        rag_config=RAGStrategyConfig(
            query="weather in London",
            max_messages=10,
            score_threshold=0.6,
        ),
    )

    # Display optimized context
    print("Optimized context:")
    for message in optimized_context:
        print(f"{message.role}: {message.content}")


if __name__ == "__main__":
    asyncio.run(main())
```

The Context Manager supports several optimization strategies:

1. **Summarize**: Creates concise summaries of older messages
2. **Window**: Keeps a sliding window of recent messages
3. **RAG**: Uses semantic search to find relevant messages
4. **Trim**: Simple truncation to fit token limits

Each strategy can be configured through the Context Manager's settings:
```python
context_manager = LiteContextManager(
    window_size=50,  # Maximum messages in sliding window
    preserve_recent=25,  # Messages to keep when summarizing
    relevant_window_size=10,  # Maximum relevant messages to return
    chunk_size=10,  # Messages per summary chunk
    default_strategy="trim",  # Default optimization strategy
    default_embedding_model="text-embedding-3-small",  # Default model for embeddings
)
```

See [ContextManager](liteswarm/core/context_manager.py) for more details.

## Basic Usage

### Simple Agent

```python
import asyncio

from liteswarm.core import Swarm
from liteswarm.types import LLM, Agent


async def main() -> None:
    # Create an agent
    agent = Agent(
        id="assistant",
        instructions="You are a helpful AI assistant.",
        llm=LLM(
            model="claude-3-5-sonnet-20241022",
            temperature=0.7,
        ),
    )

    # Create swarm and execute
    swarm = Swarm()
    result = await swarm.execute(
        agent=agent,
        prompt="Hello!",
    )

    print(result.content)


if __name__ == "__main__":
    asyncio.run(main())
```

### Agent with Tools

```python
import asyncio

from liteswarm.core import Swarm
from liteswarm.types import LLM, Agent


async def main() -> None:
    def calculate_sum(a: int, b: int) -> int:
        """Calculate the sum of two numbers."""
        return a + b

    # Create a math agent with tools
    agent = Agent(
        id="math_agent",
        instructions="Use tools for calculations. Never calculate yourself.",
        llm=LLM(
            model="claude-3-5-sonnet-20241022",
            tools=[calculate_sum],
            tool_choice="auto",
        ),
    )

    # Create swarm and execute
    swarm = Swarm()
    result = await swarm.execute(
        agent=agent,
        prompt="What is 2 + 2?",
    )

    print(result.content)


if __name__ == "__main__":
    asyncio.run(main())
```

## Event Streaming

LiteSwarm provides a powerful event streaming API that allows real-time monitoring of agent interactions:

```python
import asyncio

from liteswarm.core import Swarm
from liteswarm.types import LLM, Agent


async def main() -> None:
    agent = Agent(
        id="assistant",
        instructions="You are a helpful assistant.",
        llm=LLM(model="gpt-4o"),
    )

    swarm = Swarm()
    stream = swarm.stream(agent, prompt="Hello!")

    # Method 1: Process events with if/else branching
    async for event in stream:
        if event.type == "agent_response_chunk":
            # Handle content updates
            if content := event.chunk.completion.delta.content:
                print(content, end="", flush=True)
            # Handle completion
            if event.chunk.completion.finish_reason:
                print("\nFinished:", event.chunk.completion.finish_reason)
        elif event.type == "agent_switch":
            # Handle agent switching
            prev_id = event.previous.id if event.previous else "None"
            print(f"\nSwitching from {prev_id} to {event.current.id}")
        elif event.type == "tool_call_result":
            # Handle tool execution results
            print(f"\nTool result: {event.tool_call_result.result}")
        elif event.type == "error":
            # Handle errors
            print(f"\nError: {event.error}")

    # Get final result after streaming
    result = await stream.get_result()
    print(f"\nFinal result: {result.content}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Event Types

LiteSwarm emits several types of events during execution:

* **AgentResponseChunkEvent**:
   - Content updates from the agent
   - Completion status and reason
   - Usage statistics and cost info

* **AgentSwitchEvent**:
   - Previous and current agent IDs
   - Switching context and reason

* **ToolCallResultEvent**:
   - Tool execution results
   - Tool call metadata
   - Execution status

* **ErrorEvent**:
   - Error details and type
   - Agent context
   - Stack trace if available

* **CompleteEvent**:
   - Final conversation state
   - Complete message history
   - Execution metadata

See [SwarmEvent page](liteswarm/types/events.py) for more details.

### Custom Event Handlers

You can create custom event handlers for more sophisticated event processing. There are two main ways to handle events:

1. Using the streaming API directly (recommended for most cases):
```python
stream = swarm.stream(agent, prompt="Hello!")
async for event in stream:
    if event.type == "agent_response_chunk":
        print(event.chunk.completion.delta.content, end="", flush=True)
    elif event.type == "tool_call_result":
        print(f"\nTool: {event.tool_call_result.tool_call.function.name}")
    elif event.type == "error":
        print(f"\nError: {event.error}")
```

2. Using a custom event handler with `execute()` (useful for advanced event handling or non-async contexts):
```python
import asyncio

from typing_extensions import override

from liteswarm.core import Swarm, SwarmEventHandler
from liteswarm.types import LLM, Agent, SwarmEvent


class CustomHandler(SwarmEventHandler):
    @override
    async def on_event(self, event: SwarmEvent) -> None:
        if event.type == "agent_response_chunk":
            # Process content updates
            if content := event.chunk.completion.delta.content:
                print(content, end="", flush=True)

            # Track completion
            if event.chunk.completion.finish_reason:
                print(f"\nFinished: {event.chunk.completion.finish_reason}")

        elif event.type == "agent_switch":
            # Log agent switches
            prev_id = event.previous.id if event.previous else "None"
            print(f"\nSwitching agents: {prev_id} -> {event.current.id}")

        elif event.type == "tool_call_result":
            # Process tool results
            print(f"\nTool executed: {event.tool_call_result.tool_call.function.name}")
            print(f"Result: {event.tool_call_result.result}")

        elif event.type == "error":
            # Handle errors
            print(f"\nError occurred: {event.error}")

        elif event.type == "complete":
            # Process completion
            print("\nExecution completed")
            print(f"Messages: {len(event.messages)}")


async def main() -> None:
    agent = Agent(
        id="assistant",
        instructions="You are a helpful assistant.",
        llm=LLM(model="gpt-4o"),
    )

    swarm = Swarm()
    result = await swarm.execute(
        agent=agent,
        prompt="Hello!",
        event_handler=CustomHandler(),
    )

    print(f"\n\nResult: {result.model_dump_json(indent=2, exclude_none=True)}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Streaming with Result Collection

The `stream()` method returns an async generator that supports both event streaming and result collection:

```python
import asyncio

from liteswarm.core import Swarm
from liteswarm.types import LLM, Agent


async def main() -> None:
    agent = Agent(
        id="assistant",
        instructions="You are a helpful assistant.",
        llm=LLM(model="gpt-4o"),
    )

    swarm = Swarm(
        include_usage=True,
        include_cost=True,
    )

    # Stream events and collect result
    stream = swarm.stream(agent, prompt="Hello!")

    # Process events during execution
    async for event in stream:
        if event.type == "agent_response_chunk":
            print(event.chunk.completion.delta.content, end="", flush=True)

    # Get final result after completion
    result = await stream.get_result()
    print(f"\nFinal content: {result.content}")

    # Access metadata
    if result.usage:
        print(f"Tokens used: {result.usage.total_tokens}")

    if result.response_cost:
        prompt_cost = result.response_cost.prompt_tokens_cost
        completion_cost = result.response_cost.completion_tokens_cost
        total_cost = prompt_cost + completion_cost
        print(f"Cost: ${total_cost}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Event-Driven Architecture

LiteSwarm's event system enables:

1. **Real-time Updates**:
   - Stream content as it's generated
   - Monitor agent state changes
   - Track tool execution progress

2. **Custom Processing**:
   - Filter and transform events
   - Implement custom logging
   - Build interactive UIs

3. **Error Handling**:
   - Catch and process errors
   - Implement recovery strategies
   - Monitor execution health

4. **Progress Tracking**:
   - Monitor token usage
   - Track execution costs
   - Measure response times

## Advanced Features

### Agent Switching

Agents can dynamically switch to other agents during execution:

```python
import asyncio
import json

from liteswarm.core import Swarm
from liteswarm.types import LLM, Agent, ToolResult
from liteswarm.utils import dump_messages


async def main() -> None:
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    # Create a math agent with tools
    math_agent = Agent(
        id="math",
        instructions="You are a math expert.",
        llm=LLM(
            model="gpt-4o",
            tools=[multiply],
            tool_choice="auto",
        ),
    )

    def switch_to_math() -> ToolResult:
        """Switch to math agent for calculations."""
        return ToolResult(
            content="Switching to math expert",
            agent=math_agent,
        )

    # Create the main agent with switch tool
    main_agent = Agent(
        id="assistant",
        instructions="Help users and switch to math agent for calculations.",
        llm=LLM(
            model="gpt-4o",
            tools=[switch_to_math],
            tool_choice="auto",
        ),
    )

    # Agent will automatically switch when needed
    swarm = Swarm()
    await swarm.execute(
        agent=main_agent,
        prompt="What is 234 * 567?",
    )

    # Print the full conversation history
    messages = await swarm.message_store.get_messages()
    print(json.dumps(dump_messages(messages), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
```

> **Note:** LiteSwarm requires explicitly passing the agent you want to use in each `execute()` or `stream()` call. To maintain a conversation with the same agent, pass that agent in subsequent calls. The conversation history is preserved, but the active agent is determined by what you pass to these methods:
> ```python
> # Start with agent1
> result1 = await swarm.execute(agent1, prompt="Start task")
> 
> # Continue with agent1
> result2 = await swarm.execute(agent1, prompt="Continue task")
> 
> # Switch to agent2 (history is preserved)
> result3 = await swarm.execute(agent2, prompt="Review work")
> ```

### Agent Teams

The SwarmTeam class (from `liteswarm.experimental`) provides an experimental framework for orchestrating complex agent workflows with automated planning. It follows a two-phase process:

1. **Planning Phase**: 
   - Analyzes the prompt to create a structured plan
   - Breaks down work into specific tasks with dependencies
   - Supports interactive feedback loop for plan refinement
   - Validates task types and team capabilities

2. **Execution Phase**:
   - Executes tasks in dependency order
   - Assigns tasks to capable team members
   - Tracks progress and maintains execution state
   - Produces an artifact with results and updates

Here's a complete example:

```python
import asyncio
import json
from typing import Literal

from pydantic import BaseModel
from typing_extensions import override

from liteswarm.core import ConsoleEventHandler, Swarm
from liteswarm.experimental import SwarmTeam
from liteswarm.types import (
    LLM,
    Agent,
    ArtifactStatus,
    ContextVariables,
    Plan,
    PlanFeedbackHandler,
    Task,
    TaskDefinition,
    TeamMember,
)


# 1. Define task types and outputs
class WriteDocTask(Task):
    type: Literal["write_documentation"]
    topic: str
    target_audience: Literal["beginner", "intermediate", "advanced"]


class ReviewDocTask(Task):
    type: Literal["review_documentation"]
    content: str
    criteria: list[str]


class Documentation(BaseModel):
    content: str
    examples: list[str]
    see_also: list[str]


class ReviewFeedback(BaseModel):
    approved: bool
    issues: list[str]
    suggestions: list[str]


# 2. (Optional) Create interactive feedback handler
class InteractiveFeedback(PlanFeedbackHandler):
    @override
    async def handle(
        self,
        plan: Plan,
        prompt: str,
        context: ContextVariables | None,
    ) -> tuple[str, ContextVariables | None] | None:
        print("\nProposed plan:")
        for task in plan.tasks:
            print(f"- {task.title}")

        if input("\nApprove? [y/N]: ").lower() != "y":
            return "Please revise the plan", context
        else:
            return None


async def main() -> None:
    # 3. Create task definitions
    def build_write_doc_instructions(
        task: WriteDocTask,
        context: ContextVariables,
    ) -> str:
        return f"""
        Write a {task.target_audience}-level documentation about {task.topic}.

        Style Guide from context:
        {context.style_guide}

        You must return a JSON object that matches the following schema:
        {json.dumps(Documentation.model_json_schema())}
        """

    write_doc = TaskDefinition(
        task_type=WriteDocTask,
        instructions=build_write_doc_instructions,
        response_format=Documentation,
    )

    def build_review_doc_instructions(
        task: ReviewDocTask,
        context: ContextVariables,
    ) -> str:
        return f"""
        Review the following documentation:
        {task.content}

        Review criteria:
        {task.criteria}

        Style Guide to check against:
        {context.style_guide}

        You must return a JSON object that matches the following schema:
        {json.dumps(ReviewFeedback.model_json_schema())}
        """

    review_doc = TaskDefinition(
        task_type=ReviewDocTask,
        instructions=build_review_doc_instructions,
        response_format=ReviewFeedback,
    )

    # 4. Create specialized agents
    writer = Agent(
        id="tech_writer",
        instructions="""You are an expert technical writer who creates clear,
        concise documentation with practical examples.""",
        llm=LLM(
            model="gpt-4o",
            temperature=0.7,
        ),
    )

    reviewer = Agent(
        id="doc_reviewer",
        instructions="""You are a documentation reviewer who ensures accuracy,
        clarity, and completeness of technical documentation.""",
        llm=LLM(
            model="gpt-4o",
            temperature=0.3,  # Lower temperature for more consistent reviews
        ),
    )

    # 5. Create team members
    writer_member = TeamMember(
        id="writer",
        agent=writer,
        task_types=[WriteDocTask],
    )

    reviewer_member = TeamMember(
        id="reviewer",
        agent=reviewer,
        task_types=[ReviewDocTask],
    )

    # 6. Create swarm team
    event_handler = ConsoleEventHandler()
    swarm = Swarm(event_handler=event_handler)
    team = SwarmTeam(
        swarm=swarm,
        members=[writer_member, reviewer_member],
        task_definitions=[write_doc, review_doc],
        event_handler=event_handler,
    )

    # 7. Execute the user request
    artifact = await team.execute(
        prompt="Create beginner-friendly documentation about Python list comprehensions",
        context=ContextVariables(
            style_guide="""
            - Use simple language
            - Include practical examples
            - Link to related topics
            - Start with basic concepts
            - Show common patterns
            """
        ),
        feedback_handler=InteractiveFeedback(),
    )

    # 8. Inspect and print the results
    if artifact.status == ArtifactStatus.COMPLETED:
        print("\nDocumentation Team Results:")
        for result in artifact.task_results:
            print(f"\nTask: {result.task.type}")

            if not result.output:
                continue

            match result.output:
                case Documentation() as doc:
                    print("\nContent:")
                    print(doc.content)
                    print("\nExamples:")
                    for example in doc.examples:
                        print(f"• {example}")
                    print("\nSee Also:")
                    for ref in doc.see_also:
                        print(f"• {ref}")

                case ReviewFeedback() as review:
                    print("\nReview Feedback:")
                    print(f"Approved: {review.approved}")
                    if review.issues:
                        print("\nIssues:")
                        for issue in review.issues:
                            print(f"• {issue}")
                    if review.suggestions:
                        print("\nSuggestions:")
                        for suggestion in review.suggestions:
                            print(f"• {suggestion}")


if __name__ == "__main__":
    asyncio.run(main())
```

The SwarmTeam will:
1. Create a plan with appropriate tasks and dependencies
2. Allow plan review/modification through feedback handler
3. Execute tasks in correct order using capable team members
4. Produce an artifact containing all results and updates

See the [software_team example](examples/software_team/run.py) for a complete implementation of a development team workflow.

### Streaming with Structured Outputs

LiteSwarm provides two layers of structured output handling with real-time streaming support:

```python
import asyncio

from pydantic import BaseModel

from liteswarm.core import Swarm
from liteswarm.types import LLM, Agent


class EntitiesModel(BaseModel):
    attributes: list[str]
    colors: list[str]
    animals: list[str]


async def main() -> None:
    # Create an agent for entity extraction
    agent = Agent(
        id="extract-entities-agent",
        instructions="You're an extraction agent. Extract the entities from the input text.",
        llm=LLM(
            model="gpt-4o",
            response_format=EntitiesModel,
        ),
    )

    # Create swarm and get stream
    swarm = Swarm()
    stream = swarm.stream(
        agent,
        prompt="The quick brown fox jumps over the lazy dog with piercing blue eyes",
    )

    # Method 1: Stream responses and handle parsed content
    print("Streaming responses:")
    async for event in stream:
        if event.type == "agent_response_chunk":
            response_chunk = event.chunk
            completion = response_chunk.completion

            # Handle raw content
            if completion.delta.content is not None:
                print(completion.delta.content, end="", flush=True)

            # Handle structured outputs
            if isinstance(response_chunk.parsed_content, EntitiesModel):
                print("\nParsed content:")
                print(response_chunk.parsed_content.model_dump_json(indent=2))

    # Method 2: Get final result with parsed content
    result = await stream.get_result()
    if isinstance(result.parsed_content, EntitiesModel):
        print("\n\nFinal parsed result:")
        print(result.parsed_content.model_dump_json(indent=2))

    # Method 3: Direct execution with structured output
    print("\n\n")
    print("=" * 80)
    print("Direct execution:")
    print("=" * 80)

    result = await swarm.execute(
        agent,
        prompt="The quick brown fox jumps over the lazy dog with piercing blue eyes",
    )

    if isinstance(result.parsed_content, EntitiesModel):
        print("\nParsed result:")
        print(result.parsed_content.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
```

The example demonstrates:

1. **Real-time Content Streaming**: 
   - Stream raw content as it's generated
   - Access structured output when parsing completes
   - Handle both raw and parsed content in same stream

2. **Structured Output Handling**:
   - Define output schema with Pydantic
   - Configure agent with response format
   - Access parsed content through events

3. **Multiple Access Methods**:
   - Stream events for real-time updates
   - Get final result for complete response
   - Access both raw and parsed content

The streaming API provides:
- `event.chunk.completion.delta.content`: Raw content updates
- `event.chunk.parsed_content`: Parsed structured output
- `event.chunk.completion.finish_reason`: Completion status
- `event.chunk.completion.usage`: Token usage statistics
- `event.chunk.completion.response_cost`: Cost tracking (if enabled)

See [examples/structured_outputs/run.py](examples/structured_outputs/run.py) for more examples of different structured output strategies.

### Error Handling

LiteSwarm provides comprehensive error handling with built-in retry mechanisms. The framework automatically retries failed operations with exponential backoff:

```python
import asyncio

from liteswarm.core import Swarm
from liteswarm.types import LLM, Agent
from liteswarm.types.exceptions import RetryError, SwarmError


async def main() -> None:
    # Create swarm with custom retry settings
    swarm = Swarm(
        # Retry Configuration
        max_retries=3,  # Maximum number of retry attempts
        initial_retry_delay=1.0,  # Initial delay between retries (seconds)
        max_retry_delay=10.0,  # Maximum delay between retries (seconds)
        backoff_factor=2.0,  # Exponential backoff multiplier
    )

    agent = Agent(
        id="assistant",
        instructions="You are a helpful assistant.",
        llm=LLM(model="gpt-4o"),
    )

    # The framework will automatically:
    # 1. Retry failed API calls with exponential backoff
    # 2. Handle transient errors (network issues, rate limits)
    # 3. Preserve conversation state between retries
    # 4. Track and expose retry statistics

    try:
        stream = swarm.stream(agent, prompt="Hello!")
        async for response in stream:
            print(response.delta.content, end="", flush=True)

        result = await stream.get_result()
        print("\nFinal:", result.content)

    except RetryError as e:
        # RetryError includes:
        # - Original error that caused retries
        # - Number of retry attempts made
        # - Total retry duration
        # - Backoff strategy details
        print(f"Retry mechanism failed after {e.attempts} attempts: {e}")
        print(f"Original error: {e.original_error}")
        print(f"Total retry duration: {e.total_duration}s")

    except SwarmError as e:
        print(f"Other swarm error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
```

The framework provides automatic retry with exponential backoff for:

1. **API Calls**: Handles transient API issues
   - Network connectivity problems
   - Rate limit errors
   - Temporary service outages
   - Timeout errors

2. **Response Generation**: Manages streaming issues
   - Incomplete or malformed responses
   - Connection drops during streaming
   - Token limit exceeded errors
   - Model-specific failures

3. **Agent Switching**: Handles transition errors
   - Failed agent initialization
   - Context transfer issues
   - Tool execution failures
   - State management errors

The retry mechanism features:

1. **Exponential Backoff**: Gradually increases delay between retries
   ```python
   # Example retry delays with default settings:
   # Attempt 1: 1.0 seconds
   # Attempt 2: 2.0 seconds
   # Attempt 3: 4.0 seconds
   # Attempt 4: 8.0 seconds (capped at max_retry_delay)
   swarm = Swarm(
       max_retries=3,
       initial_retry_delay=1.0,
       max_retry_delay=10.0,
       backoff_factor=2.0,
   )
   ```

2. **State Preservation**: Maintains conversation context
   - Preserves message history
   - Retains agent state
   - Keeps tool execution results
   - Maintains parsed content

3. **Detailed Error Information**: Provides comprehensive error data
   ```python
   try:
       result = await swarm.execute(agent, prompt)
   except RetryError as e:
       print(f"Attempts: {e.attempts}")
       print(f"Duration: {e.total_duration}s")
       print(f"Original error: {e.original_error}")
       print(f"Backoff strategy: {e.backoff_strategy}")
   ```

4. **Customizable Behavior**: Configure retry settings
   ```python
   swarm = Swarm(
       # Retry settings
       max_retries=5,              # More retry attempts
       initial_retry_delay=0.5,    # Start with shorter delays
       max_retry_delay=30.0,      # Allow longer maximum delay
       backoff_factor=3.0,        # More aggressive backoff
   )
   ```

The framework also provides specific error types for different failure scenarios:

* **SwarmError**: Base class for all swarm-specific errors
   - Provides context about what went wrong
   - Contains the original exception if applicable
   - Includes agent information when relevant

* **CompletionError**: Raised when LLM completion fails permanently
   - Indicates API call failure after all retries
   - Contains the original API error
   - Provides completion attempt details

* **ContextLengthError**: Raised when context becomes too large
   - Indicates when message history exceeds limits
   - Provides details about context size
   - Suggests using memory management

* **SwarmTeamError**: Base class for team-related errors
   - Provides unified error handling for team operations
   - Contains original error and team context
   - Used for planning and execution failures

* **PlanValidationError**: Raised when plan validation fails
   - Indicates invalid task types or dependencies
   - Lists specific validation failures
   - Helps identify plan structure issues

* **TaskExecutionError**: Raised when task execution fails
   - Contains task and assignee information
   - Provides execution failure details
   - Helps track which task and member failed

* **ResponseParsingError**: Raised when response parsing fails
   - Contains raw response and expected format
   - Helps debug format mismatches
   - Used for structured output validation

* **ResponseRepairError**: Raised when response repair fails
   - Indicates failed attempts to fix invalid responses
   - Contains repair attempt details
   - Used when response cannot be salvaged

* **MaxAgentSwitchesError**: Raised when too many agent switches occur
   - Indicates potential infinite switching loops
   - Shows switch count and limit
   - Includes agent switch history

* **MaxResponseContinuationsError**: Raised when response needs too many continuations
    - Indicates when response exceeds length limits
    - Shows continuation count and limit
    - Suggests breaking task into smaller parts

* **RetryError**: Raised when retry mechanism fails
    - Contains original error that caused retries
    - Shows retry count and settings
    - Includes backoff strategy details

Best practices for error handling:

1. **Use Specific Handlers**: Catch specific errors for targeted handling
   ```python
   try:
       result = await swarm.execute(agent, prompt)
   except CompletionError as e:
       # Handle API failures
   except ContextLengthError as e:
       # Handle context length issues
   except SwarmError as e:
       # Handle other swarm errors
   ```

2. **Team Error Recovery**: Handle team-specific errors
   ```python
   try:
       artifact = await team.execute_plan(plan)
   except PlanValidationError as e:
       # Handle invalid plan structure
   except TaskExecutionError as e:
       # Handle task execution failures
   except ResponseParsingError as e:
       # Handle response format issues
   except SwarmTeamError as e:
       # Handle other team errors
   ```

3. **Response Format Recovery**: Handle parsing and repair
   ```python
   try:
       result = await team.execute_task(task)
   except ResponseParsingError as e:
       # Try to repair the response
       repaired = repair_json(e.response)
       result = parse_response(repaired, e.response_format)
   except ResponseRepairError as e:
       # Handle unrecoverable format issues
   ```

4. **Retry Configuration**: Customize retry behavior
   ```python
   swarm = Swarm(
       max_retries=3,
       initial_retry_delay=1.0,
       max_retry_delay=10.0,
       backoff_factor=2.0,
   )
   ```

### Context Variables

Context variables let you pass data between interactions. Here's a simple example:

```python
import asyncio
import json

from liteswarm.core import Swarm
from liteswarm.types import LLM, Agent, ContextVariables, ToolResult

mock_database = {
    "alice": {
        "language": "Python",
        "experience": "intermediate",
        "interests": ["web", "data science"],
    }
}


async def main() -> None:
    def get_user_preferences(user_id: str) -> ToolResult:
        """Get user preferences from a simulated database."""
        user_preferences = mock_database.get(user_id, {})
        return ToolResult(
            content=f"Found preferences for {user_id}: {user_preferences}",
            context_variables=ContextVariables(
                user_preferences=user_preferences,
                learning_path=[],  # Initialize empty learning path
            ),
        )

    def update_learning_path(topic: str, completed: bool = False) -> ToolResult:
        """Update the user's learning path with a new topic or mark as completed."""
        return ToolResult(
            content=f"{'Completed' if completed else 'Added'} topic: {topic}",
            context_variables=ContextVariables(
                topic=topic,
                completed=completed,
            ),
        )

    # Create an agent with tools
    agent = Agent(
        id="tutor",
        instructions=lambda context_variables: f"""
        You are a programming tutor tracking a student's learning journey.

        Current Context:
        - User ID: {json.dumps(context_variables.get('user_id', 'unknown'))}
        - User Preferences: {json.dumps(context_variables.get('user_preferences', {}))}
        - Learning Path: {json.dumps(context_variables.get('learning_path', []))}
        - Last Topic: {json.dumps(context_variables.get('topic', None))}
        - Last Topic Completed: {json.dumps(context_variables.get('completed', False))}

        Track their progress and suggest next steps based on their preferences and current progress.
        """,
        llm=LLM(
            model="gpt-4o",
            tools=[get_user_preferences, update_learning_path],
            tool_choice="auto",
            temperature=0.3,
        ),
    )

    # Create swarm and execute with initial context
    swarm = Swarm()

    # First interaction - get user preferences
    result = await swarm.execute(
        agent=agent,
        prompt="Start Alice's learning journey",
        context_variables=ContextVariables(user_id="alice"),
    )
    print("\nInitial Setup:", result.content)

    # Second interaction - suggest first topic
    result = await swarm.execute(
        agent=agent,
        prompt="What should Alice learn first?",
        # Context variables are preserved from the previous execution
    )
    print("\nFirst Topic Suggestion:", result.content)

    # Third interaction - mark progress and get next topic
    result = await swarm.execute(
        agent=agent,
        prompt="Alice completed the first topic. What's next?",
        # Context variables are preserved from the previous execution
    )
    print("\nProgress Update:", result.content)


if __name__ == "__main__":
    asyncio.run(main())
```

### Structured Outputs

LiteSwarm provides two layers of structured output handling:

1. **LLM-level Response Format**:
   - Set via `response_format` in `LLM` class
   - Provider-specific structured output support
   - For OpenAI/Anthropic: Direct JSON schema enforcement
   - For other providers: Manual prompt engineering

2. **Framework-level Response Format**:
   - Set in `TaskDefinition` and `PlanningAgent`
   - Provider-agnostic parsing and validation
   - Supports both Pydantic models and custom parsers
   - Handles response repair and validation

Using Swarm directly with LLM-level response format:

```python
import asyncio

from pydantic import BaseModel

from liteswarm.core import Swarm
from liteswarm.types import LLM, Agent

CODE_TO_REVIEW = """
def calculate_sum(a: int, b: int) -> int:
    \"\"\"Calculate the sum of two numbers.\"\"\"
    return a - b
"""


class ReviewOutput(BaseModel):
    issues: list[str]
    approved: bool


async def main() -> None:
    agent = Agent(
        id="reviewer",
        instructions="Review code and provide structured feedback",
        llm=LLM(
            model="gpt-4o",
            response_format=ReviewOutput,  # Direct OpenAI JSON schema support
        ),
    )

    swarm = Swarm()
    result = await swarm.execute(
        agent=agent,
        prompt=f"Review the code and provide structured feedback:\n{CODE_TO_REVIEW}",
    )

    if not isinstance(result.parsed_content, ReviewOutput):
        print("Agent failed to produce a response of type ReviewOutput")
        return

    if result.parsed_content.issues:
        print("Issues:")
        for issue in result.parsed_content.issues:
            print(f"- {issue}")

    print(f"\nApproved: {result.parsed_content.approved}")


if __name__ == "__main__":
    asyncio.run(main())
```

Using SwarmTeam with both layers (recommended for complex workflows):

```python
import asyncio
from typing import Literal

from pydantic import BaseModel

from liteswarm.core import ConsoleEventHandler, Swarm
from liteswarm.experimental import LitePlanningAgent, SwarmTeam
from liteswarm.types import (
    LLM,
    Agent,
    ArtifactStatus,
    ContextVariables,
    Plan,
    Task,
    TaskDefinition,
    TeamMember,
)

CODE_TO_REVIEW = """
def calculate_sum(a: int, b: int) -> int:
    \"\"\"Calculate the sum of two numbers.\"\"\"
    return a - bs  # Bug: Typo in variable name and wrong operator
"""


# 1. Define data structures for the review process
class ReviewTask(Task):
    type: Literal["code-review"]
    code: str
    language: str
    review_type: Literal["general", "security", "performance"]


class CodeReviewOutput(BaseModel):
    issues: list[str]
    approved: bool
    suggested_fixes: list[str]


class CodeReviewPlan(Plan):
    tasks: list[ReviewTask]


# 2. Create prompt builders
def build_review_prompt(prompt: str, context: ContextVariables) -> str:
    return f"""
    You're given the following user request:
    <request>
    {prompt}
    </request>

    Here is the code to review:
    <code language="{context.get('language', '')}" review_type="{context.get('review_type', '')}">
    {context.get('code', '')}
    </code>

    Please create a review plan consisting of 1 task.
    """.strip()


async def main() -> None:
    # 3. Create task definitions
    review_def = TaskDefinition(
        task_type=ReviewTask,
        instructions=lambda task, _: f"""
        Review the provided code focusing on {task.review_type} aspects.
        <code language="{task.language}">{task.code}</code>
        """,
        response_format=CodeReviewOutput,
    )

    # 4. Create agents
    planning_agent = Agent(
        id="planning-agent",
        instructions="You are a planning agent that creates plans for code review tasks.",
        llm=LLM(model="gpt-4o", response_format=CodeReviewPlan),
    )

    review_agent = Agent(
        id="code-reviewer",
        instructions="You are an expert code reviewer.",
        llm=LLM(model="gpt-4o", response_format=CodeReviewOutput),
    )

    # 5. Create team members
    review_member = TeamMember(
        id="senior-reviewer",
        agent=review_agent,
        task_types=[ReviewTask],
    )

    # 6. Set up swarm team
    event_handler = ConsoleEventHandler()
    swarm = Swarm()
    team = SwarmTeam(
        swarm=swarm,
        members=[review_member],
        task_definitions=[review_def],
        event_handler=event_handler,
        planning_agent=LitePlanningAgent(
            swarm=swarm,
            agent=planning_agent,
            prompt_template=build_review_prompt,
            task_definitions=[review_def],
            response_format=CodeReviewPlan,
            event_handler=event_handler,
        ),
    )

    # 7. Execute review request
    artifact = await team.execute(
        prompt="Review this Python code",
        context=ContextVariables(
            code=CODE_TO_REVIEW,
            language="python",
            review_type="general",
        ),
    )

    # 8. Show results
    if artifact.status == ArtifactStatus.COMPLETED:
        for result in artifact.task_results:
            if isinstance(result.output, CodeReviewOutput):
                assert result.assignee is not None
                print(f"\nReview by: {result.assignee.id}")
                print("\nIssues found:")
                for issue in result.output.issues:
                    print(f"- {issue}")
                print("\nSuggested fixes:")
                for fix in result.output.suggested_fixes:
                    print(f"- {fix}")
                print(f"\nApproved: {result.output.approved}")


if __name__ == "__main__":
    asyncio.run(main())
```

This example demonstrates:

1. **LLM-level Format** (Provider-specific):
   - `response_format=CodeReviewOutput` in review agent's LLM
   - `response_format=CodeReviewPlan` in planning agent's LLM
   - OpenAI will enforce JSON schema at generation time

2. **Framework-level Format** (Provider-agnostic):
   - `response_format=CodeReviewOutput` in task definition
   - `response_format=CodeReviewPlan` in planning agent
   - Framework handles parsing, validation, and repair

The two-layer approach ensures:
- Structured outputs work with any LLM provider
- Automatic parsing and validation
- Consistent interface across providers
- Fallback to prompt-based formatting
- Response repair capabilities

See [examples/structured_outputs/run.py](examples/structured_outputs/run.py) for more examples of different structured output strategies.

> **Note about OpenAI Structured Outputs**
> 
> OpenAI's JSON schema support has certain limitations:
> - No default values in Pydantic models
> - No `oneOf` in union types (must use discriminated unions)
> - Some advanced Pydantic features may not be supported
>
> While LiteSwarm's base `Task` and `Plan` types are designed to be OpenAI-compatible, this compatibility must be maintained by users when subclassing these types. For example:
>
> ```python
> # OpenAI-compatible task type
> class ReviewTask(Task):
>     type: Literal["code-review"]  # Discriminator field
>     code: str                     # Required field, no default
>     language: str                 # Required field, no default
>     
>     # Not OpenAI-compatible - has default value
>     review_type: str = "general"  # Will work with other providers
> ```
>
> We provide utilities to help maintain compatibility:
> - `liteswarm.utils.pydantic` module contains helpers for:
>   - Converting Pydantic schemas to OpenAI format
>   - Restoring objects from OpenAI responses
>   - Handling schema transformations
>
> See [examples/structured_outputs/strategies/openai_pydantic.py](examples/structured_outputs/strategies/openai_pydantic.py) for practical examples of using these utilities.
>
> Remember: Base `Task` and `Plan` are OpenAI-compatible, but maintaining compatibility in subclasses is the user's responsibility if OpenAI structured outputs are needed.

## Key Concepts

1. **Agent**: An AI entity with specific instructions and capabilities
2. **Tool**: A Python function that an agent can call
3. **Swarm**: Orchestrator for agent interactions and conversations
4. **SwarmTeam**: Coordinator for multiple specialized agents
5. **Context Variables**: Dynamic data passed to agents and tools
6. **Event Handler**: Interface for processing and responding to swarm events

## Best Practices

1. Use `ToolResult` for wrapping tool return values:
   ```python
   def my_tool() -> ToolResult:
       return ToolResult(
           content="Result",
           context_variables=ContextVariables(...)
       )
   ```

2. Implement proper error handling:
   ```python
   try:
       result = await team.execute(agent, prompt)
   except TaskExecutionError as e:
       logger.error(f"Task failed: {e}")
   ```

3. Use context variables for dynamic behavior:
   ```python
   def build_instructions(context: ContextVariables) -> str:
       return f"Help {context['user_name']} with {context['task']}"
   ```

4. Leverage event handlers for real-time feedback:
   ```python
   from typing_extensions import override
   
   from liteswarm.core import Swarm, SwarmEventHandler
   from liteswarm.types import LLM, Agent, SwarmEvent

   # Method 1: Custom event handler class
   class MyEventHandler(SwarmEventHandler):
       @override
       async def on_event(self, event: SwarmEvent) -> None:
           if event.type == "agent_response_chunk":
               # Handle content updates
               if content := event.chunk.completion.delta.content:
                   print(content, end="", flush=True)
               # Track completion
               if event.chunk.completion.finish_reason:
                   print(f"\nFinished: {event.chunk.completion.finish_reason}")
           elif event.type == "tool_call_result":
               print(f"\nTool executed: {event.tool_call_result.tool_call.function.name}")
           elif event.type == "error":
               print(f"\nError: {event.error}")

   # Use with execute() method
   result = await swarm.execute(
       agent=agent,
       prompt="Hello!",
       event_handler=MyEventHandler(),
   )

   # Method 2: Direct stream processing
   stream = swarm.stream(agent, prompt="Hello!")
   async for event in stream:
       if event.type == "agent_response_chunk":
           print(event.chunk.completion.delta.content, end="", flush=True)
       elif event.type == "tool_call_result":
           print(f"\nTool: {event.tool_call_result.tool_call.function.name}")

   # Get final result after streaming
   result = await stream.get_result()
   ```

## Examples

The framework includes several example applications in the [examples/](examples/) directory:

- **Basic REPL** ([examples/repl/run.py](examples/repl/run.py)): Simple interactive chat interface showing basic agent usage
- **Calculator** ([examples/calculator/run.py](examples/calculator/run.py)): Tool usage and agent switching with a math-focused agent
- **Mobile App Team** ([examples/mobile_app/run.py](examples/mobile_app/run.py)): Complex team of agents (PM, Designer, Engineer, QA) building a Flutter app
- **Parallel Research** ([examples/parallel_research/run.py](examples/parallel_research/run.py)): Parallel tool execution for efficient data gathering
- **Structured Outputs** ([examples/structured_outputs/run.py](examples/structured_outputs/run.py)): Different strategies for parsing structured agent responses
- **Software Team** ([examples/software_team/run.py](examples/software_team/run.py)): Complete development team with planning, review, and implementation capabilities

Each example demonstrates different aspects of the framework:
```bash
# Run the REPL example
python -m examples.repl.run

# Run the calculator example
python -m examples.calculator.run

# Try the mobile app team
python -m examples.mobile_app.run

# Run the parallel research example
python -m examples.parallel_research.run

# Experiment with structured outputs
python -m examples.structured_outputs.run

# Run the software team example
python -m examples.software_team.run
```

## Contributing

We welcome contributions to LiteSwarm! We're particularly interested in:

1. **Adding Tests**: We currently have minimal test coverage and welcome contributions to:
   - Add unit tests for core functionality
   - Add integration tests for agent interactions
   - Add example-based tests for common use cases
   - Set up testing infrastructure and CI

2. **Bug Reports**: Open an issue describing:
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Your environment details
   - Any relevant code snippets

3. **Feature Requests**: Open an issue describing:
   - The use case for the feature
   - Expected behavior
   - Example code showing how it might work

4. **Code Contributions**: 
   - Fork the repository
   - Create a new branch for your feature
   - Include tests for new functionality
   - Submit a pull request with a clear description
   - Ensure CI passes and code follows our style guide

### Development setup:

```bash
# Clone the repository
git clone https://github.com/your-org/liteswarm.git
cd liteswarm

# Create virtual environment (choose one)
python -m venv .venv
# or
poetry install
# or
uv venv

# Install development dependencies
uv pip install -e ".[dev]"
# or
poetry install --with dev

# Run existing tests (if any)
pytest

# Run type checking
mypy .

# Run linting
ruff check .
```

### Code Style
- We use ruff for linting and formatting
- Type hints are required for all functions
- Docstrings should follow Google style
- New features should include tests

### Testing Guidelines
We're building our test suite and welcome contributions that:
- Add pytest-based tests
- Include both unit and integration tests
- Cover core functionality
- Demonstrate real-world usage
- Help improve test coverage
- Set up testing infrastructure

### Commit Messages
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code changes that neither fix bugs nor add features

## Citation

If you use LiteSwarm in your research or project, please cite our work:

```bibtex
@software{mozharovskii_2024_liteswarm,
    title = {{LiteSwarm: A Lightweight Framework for Building AI Agent Systems}},
    author = {Mozharovskii, Evgenii and {GlyphyAI}},
    year = {2024},
    url = {https://github.com/glyphyai/liteswarm},
    license = {MIT},
    version = {0.4.0}
}
```

## License

MIT License - see LICENSE file for details.
