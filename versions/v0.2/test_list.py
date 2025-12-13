from task_manager import add_task, list_tasks

# Create fake memory
memory = {
    "conversations": [],
    "tasks": []
}

# Add several tasks
add_task(memory, "Finish CS50P Week 4", priority="high", category="learning")
add_task(memory, "Apply to 3 companies", priority="high", category="job_search")
add_task(memory, "Build MZ v0.2.1", priority="medium", category="mz_development")
add_task(memory, "Read AI Engineering book", priority="low", category="learning")

# List all tasks
print("All tasks:")
tasks = list_tasks(memory)
for task in tasks:
    print(f"  [{task['priority'].upper()}] {task['content']} ({task['category']})")

print(f"\nTotal: {len(tasks)} tasks")

# Test filtering (won't do anything yet since all tasks are incomplete)
print("\n--- Testing filter (should be same as above) ---")
active_tasks = list_tasks(memory, filter_completed=True)
print(f"Active tasks: {len(active_tasks)}")