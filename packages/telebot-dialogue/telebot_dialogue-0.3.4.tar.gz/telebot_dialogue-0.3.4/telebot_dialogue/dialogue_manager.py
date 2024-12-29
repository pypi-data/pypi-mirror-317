from collections.abc import Callable


class Dialogue:
    """
    A class representing a dialogue with a user.
    """

    def __init__(
            self,
            user_id: int,
            handler: Callable,
            context: dict = None,
            end_func: Callable = None,
            pause_func: Callable = None,
            continue_func: Callable = None) -> None:
        """
        Initialize a new Dialogue instance.

        Args:
            user_id (int): The unique identifier for the user.
            handler (Callable): The function to handle dialogue messages.
            context (dict, optional): Initial context for the dialogue. Defaults to None.
            end_func (Callable, optional): Function to call when the dialogue ends. Defaults to None.
            pause_func (Callable, optional): Function to call when the dialogue is paused. Defaults to None.
            continue_func (Callable, optional): Function to call when the dialogue is continued. Defaults to None.
        """
        self.user_id = user_id
        self.handler = handler
        self.state = True
        self.context = context if context else {}
        self.history = []
        self.end_func = end_func
        self.pause_func = pause_func
        self.continue_func = continue_func

    def stop_dialogue(self) -> None:
        """
        Stop the dialogue and call the pause function if it exists.
        """
        self.state = False
        if self.pause_func:
            self.pause_func(self)

    def continue_dialogue(self) -> None:
        """
        Continue the dialogue and call the continue function if it exists.
        """
        self.state = True
        if self.continue_func:
            self.continue_func(self)

    def __del__(self) -> None:
        """
        Call the end function if it exists when the dialogue object is deleted.
        """
        self.state = False
        if self.end_func:
            self.end_func(self)

    def update_context(self, key, value) -> None:
        """
        Update a key-value pair in the dialogue context.

        Args:
            key: The key to update or add to the context.
            value: The value to associate with the key.
        """
        self.context[key] = value

    def get_context(self, key, default=None) -> any:
        """
        Get a value from the dialogue context.

        Args:
            key: The key to retrieve from the context.
            default: The default value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value if not found.
        """
        return self.context.get(key, default)

    def init_handler(self, message) -> None:
        """
        Initialize the message handler for a new message.

        Args:
            message: The message to handle.
        """
        self.history.append(message)
        self.handler(message, self)

    def delete_dialogue(self):
        """
        Delete the dialogue by calling the destructor.
        """
        self.__del__()

    def get_history(self) -> list:
        """
        Get the message history of the dialogue.

        Returns:
            A list containing the message history.
        """
        return self.history

    def get_state(self) -> bool:
        """
        Get the current state of the dialogue.

        Returns:
            True if the dialogue is active, False otherwise.
        """
        return self.state

    def clear_context(self):
        """
        Clear all key-value pairs from the dialogue context.
        """
        self.context.clear()

    def serialize(self) -> dict:
        """
        Serialize the dialogue object to a dictionary.

        Returns:
            A dictionary representation of the dialogue object.
        """
        return {
            "user_id": self.user_id,
            "state": self.state,
            "context": self.context,
            "history": self.history
        }

    @classmethod
    def deserialize(cls, data: dict) -> "Dialogue":
        """
        Create a Dialogue instance from a serialized dictionary.

        Args:
            data (dict): A dictionary containing serialized dialogue data.

        Returns:
            A new Dialogue instance with the deserialized data.
        """
        dialogue = cls(data["user_id"], lambda m, c: None)  # Replace with appropriate handler
        dialogue.state = data["state"]
        dialogue.context = data["context"]
        dialogue.history = data["history"]
        return dialogue

    def clear_history(self):
        """
        Clear the message history of the dialogue.
        """
        self.history = []

    def reset_dialogue(self):
        """
        Reset the dialogue to its initial state.
        """
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
            dialogue.delete_dialogue()
            del self.dialogues[user_id]
            return True

        return False

    class DialogueUpdater:
        def __init__(self, dialogue: Dialogue) -> None:
            self.dialogue = dialogue

        def __enter__(self) -> Dialogue:
            return self.dialogue

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            pass

    def update(self, user_id: int) -> 'DialogueManager.DialogueUpdater':
        """
        Create a DialogueUpdater context manager for updating a dialogue.
    
        This method allows for safe updating of a dialogue within a context manager,
        ensuring proper handling of the dialogue object.
    
        Args:
            user_id (int): The ID of the user whose dialogue should be updated.
    
        Returns:
            DialogueManager.DialogueUpdater: A context manager for updating the dialogue.
            If no dialogue is found for the given user_id, the context manager will
            contain None.
    
        Example:
            with dialogue_manager.update(user_id) as dialogue:
                if dialogue:
                    dialogue.update_context('key', 'value')
        """
        return self.DialogueUpdater(self.find_dialogue(user_id))
