# Copyright 2024 GlyphyAI

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import sys

from typing_extensions import override

from liteswarm.core.event_handler import LiteSwarmEventHandler
from liteswarm.types.events import (
    AgentResponseChunkEvent,
    AgentSwitchEvent,
    CompleteEvent,
    ErrorEvent,
    PlanCompletedEvent,
    PlanCreatedEvent,
    SwarmEvent,
    TaskCompletedEvent,
    TaskStartedEvent,
    ToolCallResultEvent,
)


class ConsoleEventHandler(LiteSwarmEventHandler):
    """Console event handler with formatted output.

    Implements an event handler that formats and displays events in the console.
    Provides:
    - Formatted output with agent identification
    - Visual indicators for different event types
    - Real-time status updates
    - Error handling with clear feedback
    - Tool usage tracking and reporting

    The handler uses various emoji indicators to make different types of events
    visually distinct and easy to follow:
    - 🔄 Agent switches
    - 🔧 Tool calls
    - 📎 Tool results
    - ❌ Errors
    - ✅ Completion

    Example:
        ```python
        handler = ConsoleEventHandler()
        swarm = Swarm(event_handler=handler)

        # Handler will automatically format output:
        # [agent_id] This is a response...
        # 🔧 [agent_id] Using tool_name
        # 📎 [agent_id] Got result: tool result
        # ✅ [agent_id] Completed
        ```

    Notes:
        - Maintains agent context between messages
        - Handles continuation indicators for long responses
        - Provides clear error feedback
        - Ensures consistent formatting across all events
    """

    def __init__(self) -> None:
        """Initialize the console handler.

        Sets up the handler with initial state for tracking the last active
        agent to manage message continuity and formatting.
        """
        self._last_agent_id: str | None = None

    @override
    async def on_event(self, event: SwarmEvent) -> None:
        """Process and display events.

        Formats and displays events with appropriate styling and context.
        Different event types get different visual treatments:
        - Responses show agent ID and content
        - Tool calls show function name and arguments
        - Errors show clear error messages
        - Completion shows success indicator

        Args:
            event: Event to process and display.

        Notes:
            - Maintains visual continuity between messages
            - Uses appropriate output streams (stdout/stderr)
            - Ensures immediate display through flushing
            - Handles multi-line formatting
        """
        match event:
            # Swarm Events
            case AgentResponseChunkEvent():
                await self._handle_response(event)
            case ToolCallResultEvent():
                await self._handle_tool_call_result(event)
            case AgentSwitchEvent():
                await self._handle_agent_switch(event)
            case ErrorEvent():
                await self._handle_error(event)
            case CompleteEvent():
                await self._handle_complete(event)

            # Swarm Team Events
            case PlanCreatedEvent():
                await self._handle_team_plan_created(event)
            case TaskStartedEvent():
                await self._handle_team_task_started(event)
            case TaskCompletedEvent():
                await self._handle_team_task_completed(event)
            case PlanCompletedEvent():
                await self._handle_team_plan_completed(event)

    async def _handle_response(self, event: AgentResponseChunkEvent) -> None:
        """Handle agent response events.

        Args:
            event: Response event to handle.
        """
        completion = event.chunk.completion
        if completion.finish_reason == "length":
            print("\n[...continuing...]", end="", flush=True)

        if content := completion.delta.content:
            agent_id = event.chunk.agent.id
            if self._last_agent_id != agent_id:
                print(f"\n[{agent_id}] ", end="", flush=True)
                self._last_agent_id = agent_id

            print(content, end="", flush=True)

        if completion.finish_reason:
            print("", flush=True)

    async def _handle_tool_call_result(self, event: ToolCallResultEvent) -> None:
        """Handle tool call result events.

        Args:
            event: Tool call result event to handle.
        """
        agent_id = event.agent.id
        tool_call = event.tool_call_result.tool_call
        tool_name = tool_call.function.name
        print(f"\n\n📎 [{agent_id}] Tool '{tool_name}' [{tool_call.id}] called", flush=True)

    async def _handle_agent_switch(self, event: AgentSwitchEvent) -> None:
        """Handle agent switch events.

        Args:
            event: Agent switch event to handle.
        """
        prev_id = event.previous.id if event.previous else "none"
        curr_id = event.current.id
        print(f"\n\n🔄 Switching from {prev_id} to {curr_id}...", flush=True)

    async def _handle_error(self, event: ErrorEvent) -> None:
        """Handle error events.

        Args:
            event: Error event to handle.
        """
        agent_id = event.agent.id if event.agent else "unknown"
        error = str(event.error)
        print(f"\n\n❌ Error from {agent_id}: {error}", file=sys.stderr, flush=True)
        self._last_agent_id = None

    async def _handle_complete(self, event: CompleteEvent) -> None:
        """Handle completion events.

        Args:
            event: Complete event to handle.
        """
        agent_id = event.agent.id if event.agent else "unknown"
        self._last_agent_id = None
        print(f"\n\n✅ [{agent_id}] Completed\n", flush=True)

    async def _handle_team_plan_created(self, event: PlanCreatedEvent) -> None:
        """Handle team plan created events.

        Args:
            event: Team plan created event to handle.
        """
        plan_id = event.plan.id
        task_count = len(event.plan.tasks)
        print(f"\n\n🔧 Plan created (task count: {task_count}): {plan_id}\n", flush=True)

    async def _handle_team_task_started(self, event: TaskStartedEvent) -> None:
        """Handle team task started events.

        Args:
            event: Team task started event to handle.
        """
        task_id = event.task.id
        assignee_id = event.task.assignee if event.task.assignee else "unknown"
        print(f"\n\n🔧 Task started: {task_id} by {assignee_id}\n", flush=True)

    async def _handle_team_task_completed(self, event: TaskCompletedEvent) -> None:
        """Handle team task completed events.

        Args:
            event: Team task completed event to handle.
        """
        task_id = event.task.id
        assignee_id = event.task.assignee if event.task.assignee else "unknown"
        task_status = event.task.status
        print(
            f"\n\n✅ Task completed: {task_id} by {assignee_id} (status: {task_status})\n",
            flush=True,
        )

    async def _handle_team_plan_completed(self, event: PlanCompletedEvent) -> None:
        """Handle team plan completed events.

        Args:
            event: Team plan completed event to handle.
        """
        plan_id = event.plan.id
        task_count = len(event.plan.tasks)
        print(f"\n\n✅ Plan completed (task count: {task_count}): {plan_id}\n", flush=True)
