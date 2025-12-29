"""
Unit tests for task_manager module
"""
import pytest
from task_manager import add_task, list_tasks, complete_task, delete_task, validate_task_input


def test_add_task_basic():
    """Test adding a simple task"""
    # Setup
    memory = {"tasks": []}
    
    # Execute
    task = add_task(memory, "Test task")
    
    # Assert (check results)
    assert task is not None
    assert task["content"] == "Test task"
    assert task["completed"] == False
    assert len(memory["tasks"]) == 1


def test_add_task_with_priority():
    """Test adding a task with priority"""
    memory = {"tasks": []}
    
    task = add_task(memory, "Important task", priority="high")
    
    assert task["priority"] == "high"
    assert task["content"] == "Important task"

def test_list_tasks_filter_completed():
    """Test that filter_completed works correctly"""
    memory = {"tasks": []}
    task1 = add_task(memory, "Task 1")
    task2 = add_task(memory, "Task 2")
    complete_task(memory, task1["id"])

    active_tasks = list_tasks(memory, filter_completed=True)
    assert len(active_tasks) == 1
    assert active_tasks[0]["content"] == "Task 2"

def test_validate_empty_content():
    """Test that validation catches empty content"""
    errors = validate_task_input("", "high", "learning", "2025-12-15")
    assert len(errors) > 0
    assert "content" in errors[0].lower()

def test_validate_invalid_priority():
    """Test that validation rejects invalid priority"""
    errors = validate_task_input("Test task", "super-high", "learning", "2025-12-15")

    assert len(errors) > 0
    assert "priority" in errors[0].lower()
    

def test_complete_task():
    """Test marking a task as complete"""
    memory = {"tasks": []}
    task = add_task(memory, "Task 1")

    # Complete the task
    complete_task(memory, task["id"])
    
    # Check if it's marked as completed
    completed_task = memory["tasks"][0]
    assert completed_task["completed"] == True
    assert completed_task["completed_at"] is not None

def test_delete_task():
    """Test deleting a task"""
    memory = {"tasks": []}
    task = add_task(memory, "Task to delete")

    # Delete the task
    delete_task(memory, task["id"])

    # Check memory is now empty
    assert len(memory["tasks"]) == 0