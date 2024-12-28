from collections.abc import Callable


class Dialogue:
    def __init__(
            self,
            user_id: int,
            handler: Callable,
            context: dict = None,
            end_func: Callable = None,
            pause_func: Callable = None,
            continue_func: Callable = None) -> None:
        self.user_id = user_id
        self.handler = handler
        self.state = True
        self.context = context if context else {}
        self.history = []
        self.end_func = end_func
        self.pause_func = pause_func
        self.continue_func = continue_func

    def stop_dialogue(self) -> None:
        self.state = False
        if self.pause_func:
            self.pause_func(self)

    def continue_dialogue(self) -> None:
        self.state = True
        if self.continue_func:
            self.continue_func(self)

    def __del__(self) -> None:
        if self.end_func:
            self.end_func(self)

    def update_context(self, key, value) -> None:
        self.context[key] = value

    def get_context(self, key, default=None) -> any:
        return self.context.get(key, default)

    def init_handler(self, message) -> None:
        self.history.append(message)
        self.handler(message, self)

    def delete_dialogue(self):
        self.__del__()

    def get_history(self) -> list:
        return self.history

    def get_state(self) -> bool:
        return self.state

    def clear_context(self):
        self.context.clear()

    def serialize(self) -> dict:
        return {
            "user_id": self.user_id,
            "state": self.state,
            "context": self.context,
            "history": self.history
        }

    @classmethod
    def deserialize(cls, data: dict) -> "Dialogue":
        dialogue = cls(data["user_id"], lambda m, c: None)  # Здесь замените обработчик на нужный
        dialogue.state = data["state"]
        dialogue.context = data["context"]
        dialogue.history = data["history"]
        return dialogue

    def clear_history(self):
        self.history = []

    def reset_dialogue(self):
        self.state = True
        self.context.clear()
        self.history.clear()

class DialogueManager:
    """
    A class to manage multiple dialogues with users.
    """

    def __init__(self) -> None:
        """
        Initialize the DialogueManager with an empty list of dialogues.
        """
        self.dialogues = {}

    def add_dialogue(self, dialogue: Dialogue, force: bool = False) -> bool:
        """
        Add a new dialogue to the manager if it doesn't already exist.

        Args:
            dialogue (Dialogue): The dialogue object to be added.
            force (bool, optional): If True, replace any existing dialogue with the same user ID. Defaults to False.
        """
        if not self.find_dialogue(dialogue.user_id) or force:
            self.dialogues[dialogue.user_id] = dialogue
            return True

        return False

    def stop_dialogue(self, user_id: int) -> bool:
        """
        Stop the dialogue for a specific user.

        Args:
            user_id: The ID of the user whose dialogue should be stopped.
        """
        dialogue = self.find_dialogue(user_id)
        if dialogue:
            dialogue.stop_dialogue()
            return True

        return False

    def handle_message(self, message) -> bool:
        """
        Handle an incoming message by routing it to the appropriate dialogue.

        Args:
            message: The incoming message object, which should have a 'from_user' attribute with an 'id' field.
        """
        user_id = message.from_user.id
        dialogue = self.find_dialogue(user_id)
        if dialogue and dialogue.state:
            dialogue.init_handler(message)
            return True

        else:
            return False

    def find_dialogue(self, user_id: int) -> Dialogue or None:
        """
        Find a dialogue for a specific user.

        Args:
            user_id: The ID of the user whose dialogue is being searched for.

        Returns:
            Dialogue: The dialogue object if found, None otherwise.
        """
        if user_id in self.dialogues:
            return self.dialogues[user_id]
        return None

    def continue_dialogue(self, user_id: int) -> bool:
        """
        Continue a previously stopped dialogue for a specific user.

        Args:
            user_id: The ID of the user whose dialogue should be continued.
        """
        dialogue = self.find_dialogue(user_id)
        if dialogue:
            dialogue.continue_dialogue()
            return True

        return False

    def finish_dialogue(self, user_id: int) -> bool:
        """
        Finish and remove a dialogue for a specific user.

        Args:
            user_id: The ID of the user whose dialogue should be finished.
        """
        dialogue = self.find_dialogue(user_id)
        if dialogue:
            del dialogue
            return True

        return False

    class DialogueUpdater:
        def __init__(self, dialogue: Dialogue) -> None:
            self.dialogue = dialogue

        def __enter__(self) -> Dialogue:
            return self.dialogue

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            pass

    def update(self, user_id: int) -> DialogueUpdater:
        return self.DialogueUpdater(self.find_dialogue(user_id))




dialogue_manager = DialogueManager()
dialogue_manager.add_dialogue(Dialogue(123, lambda m, c: print(f"User 1: {m.text}")))
print(dialogue_manager.find_dialogue(123).context)
with dialogue_manager.update(123) as dialogue:
    dialogue.update_context("key", "value")

print(dialogue_manager.find_dialogue(123).context)

