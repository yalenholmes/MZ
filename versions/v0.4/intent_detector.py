"""
Intent detection for natural language task creation
"""

def is_task_intent(user_input: str) -> bool:
    """
    Detect if user input describes a task.
    
    Args:
        user_input: What the user said
    
    Returns:
        True if it sounds like a task, False otherwise
    """
    # Negation phrases (NOT tasks)
    NEGATION_PHRASES = [
        "i don't need to",
        "i shouldn't",
        "i don't have to",
        "i won't",
        "i'm not going to"
    ]
    
    # Task creation phrases
    TASK_PHRASES = [
        "i need to",
        "i should",
        "remind me to",
        "i have to",
        "don't let me forget",
        "make sure i",
        "help me remember to",
        "i want to",
        "i must",
        "i've got to"
        "can you remind me",
        "add a task",
        "create a task"
    ]

    user_lower = user_input.lower()
    
    # Check negations first
    for phrase in NEGATION_PHRASES:
        if phrase in user_lower:
            return False

    # Check task phrases
    for phrase in   TASK_PHRASES:
        if phrase in user_lower:
            return True
        
    return False