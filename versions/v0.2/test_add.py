from task_manager import add_task

# Create a fake memory
memory = {
    "conversations": [],
    "tasks":[]
}

# Add a task
task = add_task(
    memory=memory,
    content="Finish CS50P Week 4",
    priority="high",
    category="learning",
    due_date="2025-12-15",
    reasoning="Due tomorrow and blocking other goals"
)

# Print what we got back
print("Task created")
print(f" ID: {task['id']}")
print(f" Content: {task['content']}")
print(f" Priority: {task['priority']}")
print(f" Reasoning: {task['priority_reasoning']}")

# Print how many tasks are now in memory
print(f"\nMemory now has {len(memory['tasks'])} task(s)")