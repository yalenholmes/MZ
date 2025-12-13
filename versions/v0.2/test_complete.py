from task_manager import add_task, list_tasks, complete_task, delete_task

# Create fake memory 
memory = {
    "conversations": [],
    "tasks": []
}

# Add some tasks
task1 = add_task(memory, "Task 1", priority="high")
task2 = add_task(memory, "Task 2", priority="medium")
task3 = add_task(memory, "Task 3", priority="low")

print("=== Initial tasks ===")
for task in list_tasks(memory):
    status = "✓" if task["completed"] else "○"
    print(f"  {status} {task['content']} (ID: {task['id']})")

# Complete task 1
print(f"\n=== Completing task 1 ===")
success = complete_task(memory, task1["id"])
print(f"Succedd: {success}")

# Show updated tasks
print("\n=== After completion ===")
for task in list_tasks(memory):
    status = "✓" if task["completed"] else "○"
    print(f"  {status} {task['content']}")

# Test filtering
print("\n=== Active tasks only ===")
active = list_tasks(memory, filter_completed=True)
for task in active:
    print(f" ○ {task['content']}")
print(f'Total active: {len(active)}')

# Delete task 2
print(f"\n=== Deleting task 2 ===")
success = delete_task(memory, task2["id"])
print(f"Success: {success}")

# Show final state
print("\n=== Final tasks ===")
for task in list_tasks(memory):
    status = "✓" if task["completed"] else "○"
    print(f" {status} {task['content']}")
print(f"Total tasks: {len(memory['tasks'])}")

# Test error cases
print("\n=== Testing error cases ===")
print(f"Complete fake ID: {complete_task(memory, 'fake_id')}") # Should be False
print(f"Delete fake ID: {delete_task(memory, 'fake_id')}") # Should be False