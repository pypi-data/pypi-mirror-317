# TaskManager

TaskManager is a simple Python package for managing tasks. It's designed to be used in command-line interface (CLI) applications, providing basic task management functionality.

## Description

This package was created as part of a learning project to understand Python package development and distribution. It has evolved into a more robust solution for task management, incorporating features that allow users to easily add, remove, and track tasks along with their priorities.

The TaskManager package provides functionality to:
- Add tasks to a to-do list with customizable priority levels
- Mark tasks as completed
- Remove tasks from the list
- View current tasks and completed tasks
- Generate detailed reports of tasks
- Support for both string and integer priority types

## Usage

Here's a quick example of how to use the TaskManager effectively:

```python
from ttask_manager import TaskManager

# Create a new TaskManager instance
tm = TaskManager()

# Load existing tasks (if any) from a .json file
tm.load_recent_state('~/data_file_path')

# Add multiple tasks to the to-do list
tm.add_task(("Write README","medium"), "Create setup.py", ("Push to GitHub","high"), "Test the application")

# View current to-do tasks
tm.current_state('to-do')

# Mark specific tasks as done
tm.task_done("Write README", "Test the application")

# View completed tasks
tm.current_state('done')

# Print the current state
print(tm)

# Generate a report of today's tasks
tm.report('~/a_dir_to_save_to','report_file_name.txt')

# Clear the to-do list after completing tasks
tm.clear('todo')

# Save current tasks (if any) to a .json file
tm.save_current_state('~/data_file_path')
```

This example showcases how to create a TaskManager instance, load existing tasks, manage to-do and completed tasks, generate a daily report, and reset the lists as needed.

## Features
- Add multiple tasks at once with customizable priorities
- Remove tasks from the to-do list
- Mark tasks as completed
- View current to-do list and completed tasks with formatting
- Generate customizable reports of tasks (by 'to-do', 'done', or 'all')
- Clear specific lists or reset both lists

## Development
This project was primarily created as a learning exercise in Python package development. Its simplicity is intentional, and there are no plans for significant feature additions or expansions. However, if you find a bug or have a suggestion for a minor improvement, feel free to open an issue on the GitHub repository.

## Notice

Due to the pressure of my studies, I will be taking a pause from further development on the TaskManager. Thank you for your understanding and support during this time.

## Licensing

The code in this project is licensed under MIT license.

## Author

Taha Yasser Adnan

This project is part of my journey in learning Python package development. While it may not be a groundbreaking package, it represents an important step in understanding the process of creating, packaging, and distributing Python projects.

