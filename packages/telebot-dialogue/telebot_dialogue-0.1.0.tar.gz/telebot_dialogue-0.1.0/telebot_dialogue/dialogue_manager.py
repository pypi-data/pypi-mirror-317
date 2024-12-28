from collections.abc import Callable


class Dialogue:
    def __init__(self, user_id: int, handler: Callable, context: dict = None) -> None:
        self.user_id = user_id
        self.handler = handler
        self.state = True
        self.context = context if context else {}

    def stop_dialogue(self) -> None:
        self.state = False

    def continue_dialogue(self) -> None:
        self.state = True

    def __del__(self) -> None:
        print(f"Dialogue with user {self.user_id} terminated.")

    def update_context(self, key, value) -> None:
        self.context[key] = value

    def get_context(self, key, default=None) -> any:
        return self.context.get(key, default)

    def init_handler(self, message) -> None:
        self.handler(message, self.context)


class DialogueManager:
    """
    A class to manage multiple dialogues with users.
    """

    def __init__(self) -> None:
        """
        Initialize the DialogueManager with an empty list of dialogues.
        """
        self.dialogues = []

    def add_dialogue(self, dialogue: Dialogue) -> bool:
        """
        Add a new dialogue to the manager if it doesn't already exist.

        Args:
            dialogue (Dialogue): The dialogue object to be added.
        """
        if not self.find_dialogue(dialogue.user_id):
            self.dialogues.append(dialogue)
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
        if dialogue:
            dialogue.handler(message, dialogue)
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
        for dialogue in self.dialogues:
            if dialogue.user_id == user_id:
                return dialogue
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




