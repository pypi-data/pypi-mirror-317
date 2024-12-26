# liiliepy State Management Library

A lightweight state management library for lilliepy, inspired by state management solutions like Zustand and XState.

---

## Features

1. **State Containers**: Manage global or local state in an intuitive way.
2. **Selectors**: Derive state slices to minimize unnecessary re-renders.
3. **Transitions**: (Optional) Add finite state machine (FSM) logic for more complex scenarios.

---

## Installation

Simply include the `liiliepy_state.py` file in your project.

```bash
# Clone the repository (if applicable)
git clone <repository_url>
```

---

## Quick Start

### 1. Define a Store

Create a state container to manage your application's state.

```python
from liiliepy_state import StateContainer

# Define your store
counter_store = StateContainer({"count": 0})

# Define actions
def increment():
    counter_store.set_state(lambda state: {"count": state["count"] + 1})

def decrement():
    counter_store.set_state(lambda state: {"count": state["count"] - 1})
```

---

### 2. Use the Store in liiliepy Components

Connect your store to liiliepy components using the `use_store` hook.

```python
from reactpy import component, html
from liiliepy_state import use_store
from my_store import counter_store, increment, decrement

@component
def CounterComponent():
    state, _ = use_store(counter_store)

    return html.div(
        html.button({"onClick": lambda: decrement()}, "-"),
        html.span(f"Count: {state['count']}"),
        html.button({"onClick": lambda: increment()}, "+"),
    )
```

---

### 3. Advanced Usage: Finite State Machines (FSM)

For more complex scenarios, use the `FSMContainer` to add finite state transitions.

```python
from liiliepy_state import FSMContainer

# Define state transitions
fsm_store = FSMContainer("idle", {
    "idle": {"START": "running"},
    "running": {"STOP": "idle"},
})

# Transition actions
def start():
    fsm_store.transition("START")

def stop():
    fsm_store.transition("STOP")
```

#### Component Example

```python
@component
def FSMComponent():
    state, _ = use_store(fsm_store)

    return html.div(
        html.span(f"State: {state}"),
        html.button({"onClick": lambda: start()}, "Start"),
        html.button({"onClick": lambda: stop()}, "Stop"),
    )
```

---

## Roadmap

- **Middleware Support**: Add features like logging and persistence.
- **Optimizations**: Improve performance for concurrent updates.
- **Testing**: Cover edge cases and stress-test the library.

---

## License

This project is licensed under the MIT License. Feel free to use and contribute!
