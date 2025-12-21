"""
Task management module for MZ
Handles CRUD operations for tasks
"""
import uuid
from datetime import datetime

# Define function that generated unique ids
def generate_task_id():
    # Generate a unique task ID
    return f"task_{str(uuid.uuid4())[:8]}"

def validate_task_input(content, priority, category, due_date):
    """
    Validate task inputs before adding to memory.

    Args:
        content: Task description
        priority: Priority level (high/medium/low or None)
        category: Category name or None
        due_date: Date string (YYYY-MM-DD) or None

    Returns: 
        List if errors messages (empty list if valid)
    """
    # Define valid value
    VALID_PRIORITIES = ["high", "medium", "low"]
    VALID_CATEGORIES = ["learning","job_search","mz_development","personal"]

    # Create empty error list
    errors = []

    # Check content
    if not content or len(content.strip()) == 0:
        errors.append("Task content cannot be empty")
        
    # Check priority
    if priority and priority not in VALID_PRIORITIES:
        errors.append(f"Invalid priority: {priority}. Must be one of: {VALID_PRIORITIES}")  
    
    # Check category
    if category:
        if  category not in VALID_CATEGORIES:
            errors.append(f"Invalid category: {category}. Must be one of: {VALID_CATEGORIES}")
    
    # Check due_date
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            # If we get here, it's valid - do nothing
        except ValueError:
            errors.append(f"Invalid date format: {due_date}. Must be YYYY-MM-DD")
        # Return all errors found
    return errors

def add_task(memory, content, priority=None, category=None, due_date=None, reasoning=None):
    """
    Add a new task to memory
    
    Args:
        memory: Memory dictionary
        content: Task description
        priority: high/medium/low (optional)
        category: Task category (optional)
        due_date: Due date string (optional)
        reasoning: Priority reasoning (optional)
    
    Returns:
        The created task
    """
    # Step 0
    errors = validate_task_input(content, priority, category, due_date)

    if errors:
        # Validation failed - don't create task
        # TODO: What should we do here?
        # Option 1: Print errors and return None
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f" - {error}")
            return None
        # Option 2: Raise an exception
        # Option 3: Return a dict with errors
    pass

    # If we get here, validation passed

    # Step 1: Generate a unique ID for this taskpyth
    task_id = generate_task_id()

    # Step 2: Get the current time
    created_at = datetime.now().isoformat()

    # Step 3: Create the task dictionary with all the fields
    task = {
        "id": task_id,
        "content": content,
        "priority": priority,
        "category": category,
        "due_date": due_date,
        "priority_reasoning": reasoning,
        "completed": False,
        "created_at": created_at,
        "completed_at": None
    }

    # Step 4: Add this task to memory
    memory["tasks"].append(task)

    # Step 5: Return the task we just created
    return task

def list_tasks(memory, filter_completed=False):
    """
    List all tasks
    
    Args:
        memory: Memory dictionary
        filter_completed: If True, exclude completed tasks
    
    Returns:
        List of tasks
    """
    # Get all tasks
    all_tasks = memory["tasks"]

    # If we should filter out completed tasks
    if filter_completed:
        # Only return tasks where completed is False
        return [task for task in all_tasks if not task["completed"]]
    
    # Otherwise return all tasks
    return all_tasks

def complete_task(memory, task_id):
    """Mark a task as complete"""
    # Loop through all tasks to find the matching one
    for task in memory ["tasks"]:
        # Found it! Mark as complete
        task["completed"] = True
        task["completed_at"] = datetime.now().isoformat
        return True # Success
    
    # If we get here, task wasn't found
    return False # Failure

def delete_task(memory, task_id):
    """Remove a task from memory"""
    # Loop through tasks to find the matching one
    for i, task in enumerate(memory["tasks"]):
        if task["id"] == task_id:
            # Found it! Remove from lost
            memory["tasks"].pop(i)
            return True # Success
        
    # If we get here, task wan
    