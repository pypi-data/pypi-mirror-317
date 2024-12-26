from reactpy import use_state, use_effect

class StateContainer:
    def __init__(self, initial_state):
        self.state = initial_state
        self.listeners = []
    
    def set_state(self, updater):
        if callable(updater):
            new_state = updater(self.state)
        else:
            new_state = updater
        
        if new_state != self.state:
            self.state = new_state
            for listener in self.listeners:
                listener(new_state)
    
    def subscribe(self, listener):
        self.listeners.append(listener)
        return lambda: self.listeners.remove(listener)


def use_store(store, selector=None):
    selected_state, set_selected_state = use_state(selector(store.state) if selector else store.state)

    def update_selected_state(new_state):
        if selector:
            selected_state = selector(new_state)
            set_selected_state(selected_state)
        else:
            set_selected_state(new_state)
    
    use_effect(
        lambda: store.subscribe(update_selected_state),
        [],
    )

    def set_state(updater):
        store.set_state(updater)
    
    return selected_state, set_state

class FSMContainer(StateContainer):
    def __init__(self, initial_state, transitions):
        super().__init__(initial_state)
        self.transitions = transitions

    def transition(self, event):
        if event in self.transitions[self.state]:
            self.set_state(self.transitions[self.state][event])
        else:
            raise ValueError(f"No transition for event {event} in state {self.state}")
