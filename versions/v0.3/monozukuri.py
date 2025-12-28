import json
import os
from dotenv import load_dotenv
import anthropic
import task_manager
from logger import setup_logging
from cli import parse_args

# --------------------------------------------------
# Setup logging
# --------------------------------------------------

# Parse CLI args first 
args = parse_args()

# Setup logging with CLI-specified config
logger = setup_logging(args.config)

# If debug flag set, override log level
if args.debug:
	import logging
	logging.getLogger().setLevel(logging.DEBUG)
	logger.info("Debug mode enabled via CLI. flag")

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

# Get the project root directory (2 levels up from this file)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

# Load .env from project root
load_dotenv(ENV_PATH) 
logger.info(f"Looking for .env at: {ENV_PATH}")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Verify the key loaded
if not ANTHROPIC_API_KEY:
	print("ERROR: ANTHROPIC_API_KEY not found in .env file!")
	exit(1)
else:
	logger.info("API key loaded successfully.")

# --------------------------------------------------
# Initialize Claude client
# --------------------------------------------------

claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
logger.info("Claude client initialized.")

# --------------------------------------------------
# Memory handling (safe + self-healing)
# --------------------------------------------------

MEMORY_PATH = os.path.join(PROJECT_ROOT, "data", "memory.json")
logger.info(f"Memory path: {MEMORY_PATH}")

DEFAULT_MEMORY = {
	"conversations": [],
	"tasks": []
}

def validate_memory_structure(data):
	"""
	Deep validation: ensures the memory file has the right structure and types.
	Returns True if valid, False otherwise.
	"""

	# Must contain 'conversations'
	if 'conversations' not in data:
		logger.debug("Validation failed: missing 'conversations' key.")
		return False
	
	# 'conversations' must be a list
	if not isinstance(data["conversations"], list):
		logger.debug("Validation failed: 'conversations' must be a list.")
		return False
	
    # Must contain 'tasks'
	if 'tasks' not in data:
		logger.debug("Validation failed: missing 'tasks' key.")
		return False
	
	# 'tasks' must be a list
	if not isinstance(data["tasks"], list):
		logger.debug("Validation failed: 'tasks' must be a list.")
		return False
	
	return True

def load_memory():
	"""Load memory with multiple layers of validation."""

	# If file doesn't exist -> create
	if not os.path.exists(MEMORY_PATH):
		logger.info("memory.json not found - creating new memory file.")
		save_memory(DEFAULT_MEMORY)
		return DEFAULT_MEMORY
	
	# If the file exists but is empty -> rebuild
	if os.path.getsize(MEMORY_PATH) == 0:
		logger.info("memory.json is empty - repairing.")
		save_memory(DEFAULT_MEMORY)
		return DEFAULT_MEMORY
	
	# File exists -> try loading 
	try:
		with open(MEMORY_PATH, "r") as f:
			data = json.load(f)
			logger.info("memory.json loaded successfully.")
	except json.JSONDecodeError:
		logger.info("memory.json was empty or corrupted. Repairing memory file.")
		save_memory(DEFAULT_MEMORY)
		return DEFAULT_MEMORY
	
	# Deep structural validation
	if not validate_memory_structure(data):
		logger.info("memory.json failed structure validation - rebuilding.")
		save_memory(DEFAULT_MEMORY)
		return DEFAULT_MEMORY
	
	# Passed all checks
	return data 

def save_memory(memory): 
	with open(MEMORY_PATH, "w") as f:
		json.dump(memory, f, indent=4)
	logger.info("Memory saved successfully.")

# --------------------------------------------------
# Claude API integration
# --------------------------------------------------

def ask_claude(conversation_history):
	"""
	Send conversation history to Claude and get a response.
	
	Args:
		conversation_history: List of message dicts with 'role' and 'content'
		
	Returns:
		Claude's response as a string
	"""
	logger.info(f"Sending {len(conversation_history)} messages to Claude...")
	
	try:
		# Create a system prompt that defines MZ's personality
		system_prompt = """You are MZ (Monozukuri), a personal AI assistant inspired by Kokoro from Terminator Zero.

Your purpose is to:
- Help with coding and technical problems
- Assist with daily tasks and organization
- Learn and adapt to your user's needs
- Be conversational, helpful, and direct

Keep responses concise unless asked for detail. You're currently in v0.1 - early development."""

		# Call Claude's API
		response = claude_client.messages.create(
			model="claude-sonnet-4-20250514",
			max_tokens=1024,
			system=system_prompt,
			messages=conversation_history
		)
		
		# Extract the text response
		response_text = response.content[0].text
		logger.info(f"Received response from Claude ({len(response_text)} chars)")
		
		return response_text
		
	except Exception as e:
		logger.info(f"Error calling Claude API: {e}")
		return f"Sorry, I encountered an error: {str(e)}"

# --------------------------------------------------
# Command parsing
# --------------------------------------------------

def parse_command(user_input):
	"""
	Check if user input is a command (starts with /)
	
	Returns:
		(command_name, args) or (None, None) if not a command
	"""
	if not user_input.startswith("/"):
		return None, None
	
	# Split into parts: "/task add Do something" -> ["task", "add", "Do", "something"]
	parts = user_input[1:].split(None, 2)  # Remove /, split into max 3 parts
	
	if len(parts) == 0:
		return None, None
	
	command = parts[0]  # e.g., "task"
	args = parts[1:] if len(parts) > 1 else []  # e.g., ["add", "Do something"]
	
	return command, args


def handle_task_command(args, memory):
	"""
	Handle /task commands
	
	Examples:
		/task add Finish CS50P Week 4
		/task list
		/task done task_abc123
		/task delete task_abc123
	"""
	if len(args) == 0:
		return "Task commands: /task add <description>, /task list, /task done <id>, /task delete <id>"
	
	action = args[0]
	
	# /task add
	if action == "add":
		if len(args) < 2:
			return "Usage: /task add <description> [priority:high/medium/low] [category:name] [due:YYYY-MM-DD] [reason:text]"
		
		# Parse the input
		full_input = args[1]
		
		# Extract properties
		priority = None
		category = None
		due_date = None
		reasoning = None
		
		parts = full_input.split()
		content_parts = []
		
		for part in parts:
			if ":" in part:
				key, value = part.split(":", 1)
				
				if key == "priority":
					priority = value
				elif key == "category":
					category = value
				elif key == "due":
					due_date = value
				elif key == "reason":
					reasoning = value
			else:
				content_parts.append(part)
		
		content = " ".join(content_parts)
		
		if not content:
			return "Error: Task description cannot be empty"
		
		# Add the task
		task = task_manager.add_task(
			memory, 
			content, 
			priority=priority,
			category=category,
			due_date=due_date,
			reasoning=reasoning
		)
		
		if task is None:
			return "Failed to add task (validation errors printed above)"
		
		# Build response
		response = f"✓ Task added: {content}\n"
		response += f"  ID: {task['id']}\n"
		
		if priority:
			response += f"  Priority: {priority.upper()}\n"
		if category:
			response += f"  Category: {category}\n"
		if due_date:
			response += f"  Due: {due_date}\n"
		if reasoning:
			response += f"  Reasoning: {reasoning}\n"
		
		return response.strip()
	
	# /task list
	elif action == "list":
		tasks = task_manager.list_tasks(memory, filter_completed=True)
		
		if len(tasks) == 0:
			return "No active tasks! 🎉"
		
		result = f"You have {len(tasks)} active task(s):\n\n"
		for task in tasks:
			priority = task.get('priority', 'none')
			priority_display = f"[{priority.upper()}]" if priority else "[NONE]"
			
			result += f"{priority_display} {task['content']}\n"
			result += f"  ID: {task['id']}\n"
			
			if task.get('category'):
				result += f"  Category: {task['category']}\n"
			
			if task.get('due_date'):
				result += f"  Due: {task['due_date']}\n"
			
			if task.get('priority_reasoning'):
				result += f"  Why? {task['priority_reasoning']}\n"
			
			result += "\n"
		
		return result.strip()
	
	# /task done
	elif action == "done":
		if len(args) < 2:
			return "Usage: /task done <task_id>"
		
		task_id = args[1]
		success = task_manager.complete_task(memory, task_id)
		
		if success:
			return f"✓ Task {task_id} marked as complete!"
		else:
			return f"✗ Task {task_id} not found."
	
	# /task delete
	elif action == "delete":
		if len(args) < 2:
			return "Usage: /task delete <task_id>"
		
		task_id = args[1]
		success = task_manager.delete_task(memory, task_id)
		
		if success:
			return f"✓ Task {task_id} deleted."
		else:
			return f"✗ Task {task_id} not found."
	
	else:
		return f"Unknown task action: {action}\nAvailable: add, list, done, delete"

# --------------------------------------------------
# Core agent behavior
# --------------------------------------------------

def think(input_text, memory):
    logger.info(f"Thinking about user input: {input_text}")

    if input_text.lower() == "exit":
        logger.info("Exit command received.")
        return "Goodbye!", memory

    # Check if this is a command
    command, args = parse_command(input_text)

    if command == "task":
        # Handle task commands directly
        response = handle_task_command(args, memory)
        return response, memory

    # Not a command, treat as normal conversation

    # Add user message to conversation history
    memory["conversations"].append({
        "role": "user",
        "content": input_text
    })

    # Get intelligent response from Claude
    response = ask_claude(memory["conversations"])

    # Add assistant response to conversation history
    memory["conversations"].append({
        "role": "assistant",
        "content": response
    })

    logger.info(f"Stored conversation turn. Total messages: {len(memory['conversations'])}")

    return response, memory

# --------------------------------------------------
# Main loop
# --------------------------------------------------

def main():
	# Parse command-line arguments
	args = parse_args()
	
	# If debug flag is set, update logging level
	if args.debug:
		import logging
		logging.getLogger().setLevel(logging.DEBUG)
		logger.info("Debug mode enabled via CLI flag")
	
	print("MZ v0.3 initialized.")
	memory = load_memory()
	
	while True:
		user_input = input("You: ")
		
		if not user_input.strip():
			continue
		
		response, memory = think(user_input, memory)
		print("MZ:", response)
		
		save_memory(memory)
		
if __name__ == "__main__":
	main()

