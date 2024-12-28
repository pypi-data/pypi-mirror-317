"""State machine walker module.

This module provides the base `Walker` and `StateMachine` classes for traversing state machines during parsing
and generation. Walkers track state transitions and maintain parsing history, while StateMachines manage the
constraints and transitions within the state machine.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Self, TypeVar

from pse_core import Edge, State, StateGraph, VisitedEdge

class Engine(ABC):
    """
    The core engine class that manages the state machine and walkers.
    """

    def __init__(self, reverse_vocabulary: dict[int, str]) -> None: ...
    """Initialize the engine with a reverse vocabulary (a map of token ids to tokens). The token ids are the ids used by the model. The token string representation is the decoded string of the token id."""

    @property
    def vocabulary(self) -> dict[str, int]: ...
    """The vocabulary (a map of tokens to token ids). The token string representation is the decoded string of the token id."""
    @property
    def reverse_vocabulary(self) -> dict[int, str]: ...
    """The reverse vocabulary (a map of token ids to tokens). The token string representation is the decoded string of the token id."""

    @property
    def has_reached_accept_state(self) -> bool: ...

    @property
    def within_json_value(self) -> bool: ...

    @property
    def is_encapsulated(self) -> bool: ...

    @is_encapsulated.setter
    def is_encapsulated(self, value: bool) -> None: ...

    @property
    def walkers(self) -> list[Walker]: ...

    @walkers.setter
    def walkers(self, value: list[Walker]) -> None: ...

    @abstractmethod
    def encode_token(self, token: str) -> list[int]: ...

    T = TypeVar("T")
    def process_logits(self, input_ids: Any, scores: T) -> T: ...
    """Process logits for a given input and scores"""

    def advance_token(self, token_id: int) -> int | None: ...
    """Advance the engine with the given token. Returns the advanced token or None if the token is not valid."""

    def consume_raw_input(self, input: str) -> None: ...
    """Consume raw input and advance the engine."""

    def get_trie(self) -> TrieSet: ...
    """Get the trie constructed from the vocabulary."""

class StateMachine:
    """
    A state machine that manages multiple walkers representing
    different valid states, enabling efficient traversal and minimizing backtracking.
    """

    def __init__(
        self,
        state_graph: StateGraph | None = None,
        start_state: State = 0,
        end_states: list[State] | None = None,
        is_optional: bool = False,
        is_case_sensitive: bool = True,
    ) -> None: ...


    @property
    def is_optional(self) -> bool:
        """Check if the state machine is optional."""
        ...

    @property
    def is_case_sensitive(self) -> bool:
        """Check if the state machine is case sensitive."""
        ...

    def get_new_walker(self, state: State | None = None) -> Walker:
        """Get a new walker for this state machine."""
        ...

    def get_walkers(self, state: State | None = None) -> list[Walker]:
        """Get walkers to traverse the state machine.

        Args:
            state: Optional starting state.

        Returns:
            A list of walker instances.
        """
        ...

    def get_transitions(self, walker: Walker, state: State | None = None) -> list[tuple[Walker, State, State]]:
        """Get transitions from the given walker.

        Args:
            walker: Walker to get transitions from.

        Returns:
            A list of tuples containing a walker, start state, and target state.
        """
        ...

    def get_edges(self, state: State) -> list[Edge]:
        """Get edges from the given state."""
        ...

    def branch_walker(self, walker: Walker, token: str | None = None) -> list[Walker]:
        """Branch the walker into multiple paths.

        Args:
            walker: Walker to branch.
            token: Optional token to consider.

        Returns:
            A list of branched walkers.
        """
        ...

    def advance(self, walker: Walker, token: str) -> list[Walker]:
        """Advance the walker with the given input token.

        Args:
            walker: The walker to advance.
            token: The input token to process.

        Returns:
            A list of updated walkers after advancement.
        """
        ...

    @staticmethod
    def advance_all(walkers: list[Walker], token: str, vocab: TrieSet | None = None) -> list[tuple[str, Walker]]:
        """Advance multiple walkers with a token, optionally using a vocabulary DAWG."""
        ...

    def __eq__(self, other: object) -> bool:
        """Check equality based on the state machine's state graph.

        Args:
            other: The object to compare with.

        Returns:
            True if both state machines are equal; False otherwise.
        """
        ...

    def __str__(self) -> str:
        """Return the string representation of the state machine."""
        ...

    def __repr__(self) -> str:
        """Return a detailed string representation of the state machine."""
        ...

    @property
    def start_state(self) -> State:
        """The start state of the state machine."""
        ...

    @start_state.setter
    def start_state(self, value: State) -> None: ...

    @property
    def end_states(self) -> list[State]:
        """The end states of the state machine."""
        ...

    @end_states.setter
    def end_states(self, value: list[State]) -> None: ...

    @property
    def state_graph(self) -> StateGraph:
        """The state transition graph."""
        ...

    @state_graph.setter
    def state_graph(self, value: StateGraph) -> None: ...

class Walker:
    """
    Base class for state machine walkers.

    A `Walker` represents a position in a state machine graph and manages transitions
    between states as input is consumed. It tracks the current state, transition
    history, and accumulated values during parsing or generation.
    """

    def __init__(
        self,
        state_machine: StateMachine,
        current_state: State | None = None,
    ) -> None: ...

    def clone(self) -> Self:
        """Create a clone of the walker.

        Returns:
            A new instance of the walker with the same state.
        """
        ...

    def consume_token(self, token: str) -> list[Walker]:
        """Advance the walker with the given input token.

        Args:
            token: The token to process.

        Returns:
            A list of updated walker instances after advancement.
        """
        ...

    def can_accept_more_input(self) -> bool:
        """Indicate whether the walker can accept more input for the current state.

        Returns:
            True if the walker can accept more input; False otherwise.
        """
        ...

    def is_within_value(self) -> bool:
        """Determine if the walker is currently within a value.

        Returns:
            True if in a value; False otherwise.
        """
        ...

    def should_start_transition(self, token: str) -> bool:
        """Determine if a transition should start with the given input token.

        Args:
            token: The token to process.

        Returns:
            True if the transition should start; False otherwise.
        """
        ...

    def should_complete_transition(self) -> bool:
        """Determine if the transition should complete.

        Returns:
            True if the transition should complete; False otherwise.
        """
        ...

    def accepts_any_token(self) -> bool:
        """Check if the state machine accepts any token (i.e., free text).

        Returns:
            True if all tokens are accepted; False otherwise.
        """
        ...

    def get_valid_continuations(self, depth: int = 0) -> list[str]:
        """Return the set of strings that allow valid continuation from current state.

        Args:
            depth: The current depth in the state machine traversal.

        Returns:
            A list of strings that represent valid continuations from current state.
        """
        ...

    def has_reached_accept_state(self) -> bool:
        """Check if the walker has reached an accepted (final) state.

        Returns:
            True if in an accepted state; False otherwise.
        """
        ...

    def parse_value(self, value: str | None) -> Any:
        """Parse the accumulated value into an appropriate type.

        Args:
            value: The value to parse.

        Returns:
            The parsed value.
        """
        ...

    def start_transition(
        self,
        transition_walker: Walker,
        token: str | None = None,
        start_state: State | None = None,
        target_state: State | None = None,
    ) -> Walker | None:
        """Start a new transition with the given token.

        Args:
            transition_walker: The walker handling the current transition.
            token: Optional token to consider.
            start_state: Optional starting state.
            target_state: Optional target state.

        Returns:
            A new walker instance after starting the transition or None if not possible.
        """
        ...

    def complete_transition(
        self,
        transition_walker: Walker,
    ) -> tuple[Walker | None, bool]:
        """Complete the current transition.

        Args:
            transition_walker: The walker handling the current transition.

        Returns:
            A tuple containing a new walker instance and a boolean indicating success.
        """
        ...

    def branch(self, token: str | None = None) -> list[Walker]:
        """Branch the current walker into multiple paths.

        Args:
            token: Optional token to consider.

        Returns:
            A list of branched walker instances.
        """
        ...

    def get_current_value(self) -> Any:
        """Retrieve the accumulated walker value.

        Returns:
            The current value from transition or history, parsed into appropriate type.
            Returns None if no value is accumulated.
        """
        ...

    def get_raw_value(self) -> str | None:
        """Retrieve the raw accumulated value as a string.

        Returns:
            The concatenated raw values from history and transitions.
        """
        ...

    @property
    def state_machine(self) -> StateMachine:
        """The state machine associated with this walker."""
        ...

    @state_machine.setter
    def state_machine(self, value: StateMachine) -> None: ...

    @property
    def accepted_history(self) -> list[Walker]:
        """The history of accepted walkers."""
        ...

    @accepted_history.setter
    def accepted_history(self, value: list[Walker]) -> None: ...

    @property
    def explored_edges(self) -> set[VisitedEdge]:
        """The set of explored edges."""
        ...

    @explored_edges.setter
    def explored_edges(self, value: set[VisitedEdge]) -> None: ...

    @property
    def current_state(self) -> State:
        """The current state."""
        ...

    @current_state.setter
    def current_state(self, value: State) -> None: ...

    @property
    def target_state(self) -> State | None:
        """The target state."""
        ...

    @target_state.setter
    def target_state(self, value: State | None) -> None: ...

    @property
    def transition_walker(self) -> Walker | None:
        """The transition walker."""
        ...

    @transition_walker.setter
    def transition_walker(self, value: Walker | None) -> None: ...

    @property
    def consumed_character_count(self) -> int:
        """The number of consumed characters."""
        ...

    @consumed_character_count.setter
    def consumed_character_count(self, value: int) -> None: ...

    @property
    def remaining_input(self) -> str | None:
        """The remaining input string."""
        ...

    @remaining_input.setter
    def remaining_input(self, value: str | None) -> None: ...

    @property
    def _accepts_more_input(self) -> bool:
        """Check if the walker can accept more input."""
        ...

    @_accepts_more_input.setter
    def _accepts_more_input(self, value: bool) -> None: ...

    @property
    def _raw_value(self) -> str | None:
        """The raw accumulated value as a string."""
        ...

    @_raw_value.setter
    def _raw_value(self, value: str | None) -> None: ...

    def __eq__(self, other: object) -> bool:
        """Check equality based on the walker's state and accumulated value.

        Args:
            other: The object to compare with.

        Returns:
            True if both walkers are equal; False otherwise.
        """
        ...

    def __str__(self) -> str:
        """Return the string representation of the walker."""
        ...

    def __repr__(self) -> str:
        """Return a detailed string representation of the walker."""
        ...


class AcceptedState(Walker):
    """Represents a walker that has reached an accepted state.

    This class wraps another walker (`accepted_walker`) that has successfully
    reached an accepted state in the state machine. It acts as a marker for
    accepted states and provides methods to retrieve values and advance the walker.
    """

    def __init__(self, walker: Walker) -> None:
        """Initialize the AcceptedState with the given walker.

        Args:
            walker: The walker that has reached an accepted state.
        """
        ...

    def clone(self) -> Walker:
        """Create a clone of the accepted walker.

        Returns:
            A new instance of the walker with the same state.
        """
        ...

    def can_accept_more_input(self) -> bool:
        """Check if the accepted walker can accept more input.

        Returns:
            True if the accepted walker can accept more input; False otherwise.
        """
        ...

    def has_reached_accept_state(self) -> bool:
        """Check if this walker is in an accepted state.

        Returns:
            Always `True` for `AcceptedState` instances.
        """
        ...

    def is_within_value(self) -> bool:
        """Determine if this walker is currently within a value.

        Returns:
            `False`, as accepted states are not considered to be within a value.
        """
        ...

    def should_start_transition(self, token: str) -> bool:
        """Determines if a transition should start with the given input string.

        Args:
            token: The input string to process.

        Returns:
            True if the transition should start; False otherwise.
        """
        ...

    def consume_token(self, token: str) -> list[Walker]:
        """Advance the accepted walker with the given input.

        Args:
            token: The input string to process.

        Returns:
            A list of updated walkers after advancement.
        """
        ...

    def __eq__(self, other: object) -> bool:
        """Check equality with another object.

        Args:
            other: The object to compare with.

        Returns:
            True if equal to the accepted walker; False otherwise.
        """
        ...

    def __repr__(self) -> str:
        """Return a string representation of the accepted state.

        Returns:
            A string representing the accepted state.
        """
        ...

class TrieSet:
    """A HAT-trie based set implementation for efficient string storage and lookup.

    This class provides an efficient implementation of a set data structure
    specifically optimized for string keys using a HAT-trie structure.
    """

    def __init__(self, burst_threshold: int = 1024) -> None: ...
    """Initialize a new TrieSet.

    Args:
        burst_threshold: Optional threshold for the trie's burst operation.
    """

    def insert(self, key: str) -> None: ...
    """Insert a string into the set.

    Args:
        key: The string to insert.
    """

    def insert_all(self, keys: list[str]) -> TrieSet: ...
    """Insert multiple strings into the set.

    Args:
        keys: List of strings to insert.

    Returns:
        Self for method chaining.
    """

    def erase(self, key: str) -> int: ...
    """Remove a string from the set.

    Args:
        key: The string to remove.

    Returns:
        Number of elements removed (0 or 1).
    """

    def find(self, key: str) -> bool: ...
    """Check if a string exists in the set.

    Args:
        key: The string to look for.

    Returns:
        True if the string exists in the set, False otherwise.
    """

    @property
    def empty(self) -> bool: ...
    """Check if the set is empty.

    Returns:
        True if the set contains no elements, False otherwise.
    """

    @property
    def size(self) -> int: ...
    """Get the number of elements in the set.

    Returns:
        The number of strings stored in the set.
    """

    def clear(self) -> None: ...
    """Remove all elements from the set."""
