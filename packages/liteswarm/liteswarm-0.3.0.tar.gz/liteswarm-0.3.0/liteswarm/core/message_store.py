# Copyright 2024 GlyphyAI

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import copy
import uuid
from collections.abc import Sequence
from typing import Any, Protocol, TypeVar

from typing_extensions import override

from liteswarm.types.message_store import LiteMessageStoreFilter
from liteswarm.types.messages import MessageRecord
from liteswarm.types.swarm import Message

FilterT = TypeVar("FilterT", contravariant=True)
"""Type variable for store-specific filter types."""


class MessageStore(Protocol[FilterT]):
    """Protocol for managing messages with metadata and filtering.

    Provides storage and retrieval of messages with unique IDs and custom metadata.
    Supports multiple storage backends like in-memory dictionaries, SQL databases,
    and vector stores. All operations are thread-safe and use deep copies.

    Examples:
        Basic in-memory implementation:
            ```python
            class SimpleStore(MessageStore["SimpleFilter"]):
                async def get_messages(self, filter: SimpleFilter) -> list[MessageRecord]:
                    # Filter messages based on SimpleFilter rules
                    return filtered_messages

                async def add_messages(self, messages: list[Message]) -> list[MessageRecord]:
                    # Add multiple messages atomically
                    return [await self._create_record(msg) for msg in messages]
            ```

        SQLite implementation:
            ```python
            class SQLiteFilter(BaseModel):
                role: str | None = None
                search_text: str | None = None
                tags: list[str] | None = None
                last_n: int | None = None


            class SQLiteStore(MessageStore[SQLiteFilter]):
                async def get_messages(self, filter: SQLiteFilter | None = None) -> list[MessageRecord]:
                    query = "SELECT * FROM messages"
                    params = []

                    if filter:
                        conditions = []
                        if filter.role:
                            conditions.append("role = ?")
                            params.append(filter.role)
                        if filter.search_text:
                            conditions.append("content LIKE ?")
                            params.append(f"%{filter.search_text}%")
                        if filter.tags:
                            placeholders = ",".join("?" * len(filter.tags))
                            conditions.append(f"tag IN ({placeholders})")
                            params.extend(filter.tags)

                        if conditions:
                            query += " WHERE " + " AND ".join(conditions)

                        if filter.last_n:
                            query += " ORDER BY timestamp DESC LIMIT ?"
                            params.append(filter.last_n)

                    async with self._db.execute(query, params) as cursor:
                        rows = await cursor.fetchall()
                        return [self._row_to_message(row) for row in rows]

                async def add_messages(self, messages: list[Message]) -> list[MessageRecord]:
                    async with self._db.transaction():
                        records = []
                        for message in messages:
                            record = await self._insert_message(message)
                            records.append(record)
                        return records
            ```

        Vector store implementation:
            ```python
            class VectorFilter(BaseModel):
                query: str | None = None
                similarity_threshold: float = 0.8
                max_results: int = 10
                metadata_filters: dict[str, Any] | None = None


            class VectorStore(MessageStore[VectorFilter]):
                async def get_messages(self, filter: VectorFilter | None = None) -> list[MessageRecord]:
                    if not filter or not filter.query:
                        return list(self._messages.values())

                    # Generate query embedding
                    query_embedding = await self._embed(filter.query)

                    # Search vector store
                    results = await self._vector_store.search(
                        query_embedding,
                        filter=filter.metadata_filters,
                        limit=filter.max_results,
                        min_score=filter.similarity_threshold,
                    )

                    return [self._result_to_message(r) for r in results]

                async def add_messages(self, messages: list[Message]) -> list[MessageRecord]:
                    # Batch embed and store messages
                    embeddings = await self._embed_batch([msg.content for msg in messages])
                    return await self._vector_store.add_batch(messages, embeddings)
            ```

        Redis implementation:
            ```python
            class RedisFilter(BaseModel):
                role: str | None = None
                before: datetime | None = None
                after: datetime | None = None
                last_n: int | None = None


            class RedisStore(MessageStore[RedisFilter]):
                async def get_messages(self, filter: RedisFilter | None = None) -> list[MessageRecord]:
                    # Use Redis sorted set for time-based queries
                    if not filter:
                        messages = await self._redis.zrange("messages", 0, -1)
                        return [self._deserialize(msg) for msg in messages]

                    min_score = "-inf"
                    max_score = "+inf"

                    if filter.after:
                        min_score = filter.after.timestamp()
                    if filter.before:
                        max_score = filter.before.timestamp()

                    messages = await self._redis.zrangebyscore(
                        "messages",
                        min_score,
                        max_score,
                    )

                    if filter.role:
                        messages = [
                            msg for msg in messages if self._deserialize(msg).message.role == filter.role
                        ]

                    if filter.last_n:
                        messages = messages[-filter.last_n :]

                    return [self._deserialize(msg) for msg in messages]

                async def add_messages(self, messages: list[Message]) -> list[MessageRecord]:
                    # Use Redis pipeline for atomic batch insert
                    async with self._redis.pipeline() as pipe:
                        records = []
                        for message in messages:
                            record = self._create_record(message)
                            await pipe.zadd("messages", record.timestamp, self._serialize(record))
                            records.append(record)
                        await pipe.execute()
                        return records
            ```
    """

    async def get_messages(
        self,
        filter: FilterT | None = None,
    ) -> list[MessageRecord]:
        """Get messages matching the specified filter.

        Returns filtered messages in implementation-defined order. An empty filter
        matches all messages, and an empty result is returned when no messages match.
        Messages are deep copied to prevent mutations.

        Args:
            filter: Implementation-specific filter for message retrieval.

        Returns:
            List of messages matching the filter.
        """
        ...

    async def set_messages(
        self,
        messages: Sequence[Message],
        metadata: dict[str, Any] | None = None,
    ) -> list[MessageRecord]:
        """Replace all existing messages with new ones.

        Atomically clears all existing messages and adds the provided ones. The
        optional metadata is applied to all new messages. Returns the newly created
        message records in implementation-defined order.

        Args:
            messages: Messages to store
            metadata: Optional metadata to associate with all messages

        Returns:
            List of stored message records.
        """
        ...

    async def add_message(
        self,
        message: Message,
        message_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MessageRecord:
        """Add a new message with optional ID and metadata.

        Creates a MessageRecord from the given message and stores it with a unique
        ID. If message_id is not provided, an implementation-specific ID is generated.
        The operation is atomic and thread-safe.

        Args:
            message: The message to add
            metadata: Optional metadata to associate with the message
            message_id: Optional custom ID for the message

        Returns:
            The stored message record with its ID and metadata.
        """
        ...

    async def add_messages(
        self,
        messages: Sequence[Message],
        metadata: dict[str, Any] | None = None,
    ) -> list[MessageRecord]:
        """Add multiple messages to the store.

        Atomically adds multiple messages to the store. Each message gets a unique ID
        and optional metadata. The operation preserves message order and is thread-safe.

        Args:
            messages: Messages to add to the store. Order is preserved.
            metadata: Optional metadata to associate with all messages.
                     Each message gets a deep copy of this metadata.

        Returns:
            List of stored message records in the same order as input.
        """
        ...

    async def remove_message(self, message_id: str) -> None:
        """Remove a message by its ID.

        Atomically removes the message with the given ID if it exists. The operation
        is thread-safe and has no effect if the ID doesn't exist.

        Args:
            message_id: Unique identifier of the message to remove.
        """
        ...

    async def remove_messages(
        self,
        message_ids: Sequence[str],
    ) -> None:
        """Remove multiple messages by their IDs.

        Atomically removes messages with the given IDs. The operation is thread-safe
        and skips any IDs that don't exist. If no IDs are provided, no action is taken.

        Args:
            message_ids: IDs of messages to remove. Non-existent IDs are ignored.
        """
        ...

    async def clear(self) -> None:
        """Remove all messages.

        Atomically removes all messages and their associated metadata. This operation
        is thread-safe and irreversible.
        """
        ...


class LiteMessageStore(MessageStore[LiteMessageStoreFilter]):
    """Lightweight in-memory implementation of the MessageStore protocol.

    Uses a dictionary for storage with UUID-based message IDs. Provides fast
    lookups, chronological ordering, and thread-safe operations through deep
    copying. Supports metadata association and flexible filtering with AND logic.

    Examples:
        Basic usage:
            ```python
            store = LiteMessageStore()

            # Add messages with metadata
            messages = [
                Message(role="user", content="Hello"),
                Message(role="assistant", content="Hi"),
            ]
            records = await store.add_messages(
                messages,
                metadata={"session": "greeting"},
            )

            # Filter messages
            filter = LiteMessageStoreFilter(
                role="user",
                metadata_filters={"session": "greeting"},
            )
            user_messages = await store.get_messages(filter)

            # Replace all messages
            new_messages = [
                Message(role="system", content="New conversation"),
                Message(role="user", content="Start"),
            ]
            await store.set_messages(new_messages, metadata={"session": "new"})

            # Remove specific messages
            message_ids = [record.id for record in records]
            await store.remove_messages(message_ids)
            ```
    """

    def __init__(self) -> None:
        """Initialize an empty in-memory message store.

        Creates an empty dictionary for storing messages with their IDs as keys
        and MessageRecord instances as values.
        """
        self._messages: dict[str, MessageRecord] = {}

    @override
    async def get_messages(
        self,
        filter: LiteMessageStoreFilter | None = None,
    ) -> list[MessageRecord]:
        """Get messages matching the filter criteria.

        Applies filters in sequence: role, time range, metadata, and count limit.
        Messages are sorted by timestamp before applying the count limit. Returns
        deep copies to prevent external state mutation.

        Args:
            filter: Optional criteria for filtering messages. When None, returns
                   all messages in chronological order.

        Returns:
            List of message records matching the filter criteria. If a count limit
            is specified via filter.last_n, returns only the most recent messages.
        """
        messages = list(self._messages.values())
        if filter is None:
            return copy.deepcopy(messages)

        if filter.role:
            messages = [m for m in messages if m.role == filter.role]

        if filter.before:
            messages = [m for m in messages if m.timestamp < filter.before]

        if filter.after:
            messages = [m for m in messages if m.timestamp > filter.after]

        if filter.metadata_filters:
            for key, value in filter.metadata_filters.items():
                messages = [
                    m
                    for m in messages
                    if m.metadata and key in m.metadata and m.metadata[key] == value
                ]

        if filter.last_n is not None:
            messages = messages[-filter.last_n :]

        return copy.deepcopy(messages)

    @override
    async def set_messages(
        self,
        messages: Sequence[Message],
        metadata: dict[str, Any] | None = None,
    ) -> list[MessageRecord]:
        """Replace all messages in the store.

        Atomically replaces all existing messages with new ones. Each message
        is assigned a new UUID and wrapped in a MessageRecord with the provided
        metadata. The operation maintains chronological order based on the
        sequence order.

        Args:
            messages: Sequence of messages to store. Order is preserved.
            metadata: Optional metadata to apply to all messages. Each message
                     gets a deep copy of this metadata.

        Returns:
            List of stored message records in the same order as the input sequence.
        """
        await self.clear()
        return await self.add_messages(messages, metadata=metadata)

    @override
    async def add_message(
        self,
        message: Message,
        message_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MessageRecord:
        """Add a new message to the store.

        Creates a MessageRecord with the current timestamp and stores it with
        either a provided ID or a generated UUID. The operation is atomic and
        thread-safe through dictionary key insertion.

        Args:
            message: Message to store, will be wrapped in a MessageRecord.
            message_id: Optional custom ID. If None, a UUID is generated.
            metadata: Optional metadata to associate with the message.

        Returns:
            A deep copy of the stored message record with its ID and metadata.

        Raises:
            ValueError: If the provided message_id already exists in the store.
        """
        message_id = message_id or str(uuid.uuid4())
        if message_id in self._messages:
            raise ValueError(f"Message with ID {message_id} already exists")

        record = MessageRecord.from_message(
            message=copy.deepcopy(message),
            metadata=copy.deepcopy(metadata) if metadata else {},
        )

        self._messages[message_id] = record
        return copy.deepcopy(record)

    @override
    async def add_messages(
        self,
        messages: Sequence[Message],
        metadata: dict[str, Any] | None = None,
    ) -> list[MessageRecord]:
        """Add multiple messages to the store.

        Creates MessageRecords for each message with the current timestamp and
        stores them with generated UUIDs. The operation maintains chronological
        order based on the sequence order.

        Args:
            messages: Messages to store. Order is preserved.
            metadata: Optional metadata to apply to all messages.
                     Each message gets a deep copy of this metadata.

        Returns:
            List of stored message records in the same order as input.
        """
        records: list[MessageRecord] = []

        for message in messages:
            record = await self.add_message(message, metadata=metadata)
            records.append(record)

        return records

    @override
    async def remove_message(self, message_id: str) -> None:
        """Remove a message from the store.

        Attempts to remove the message with the given ID. The operation is
        atomic through dictionary key deletion and has no effect if the ID
        doesn't exist.

        Args:
            message_id: ID of the message to remove. Non-existent IDs are ignored.
        """
        self._messages.pop(message_id, None)

    @override
    async def remove_messages(self, message_ids: Sequence[str]) -> None:
        """Remove multiple messages by their IDs.

        Attempts to remove messages with the given IDs. The operation is atomic
        through dictionary key deletion and skips any IDs that don't exist.

        Args:
            message_ids: IDs of messages to remove. Non-existent IDs are ignored.
        """
        for message_id in message_ids:
            self._messages.pop(message_id, None)

    @override
    async def clear(self) -> None:
        """Clear all messages from the store.

        Atomically removes all messages and their metadata from the store.
        The operation is thread-safe through dictionary clearing and cannot
        be undone.
        """
        self._messages.clear()
