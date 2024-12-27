import json
from json import JSONDecodeError
import os
import re
from datetime import date
from typing import List, Dict, Union, Optional, Literal, Tuple
from rich.console import Console,Theme
from rich.table import Table


class TaskManager:
    """
    TaskManager provides functionality for managing tasks, including adding, removing, marking tasks as done, 
    saving/loading task states from a JSON file, and generating task reports. Tasks can be assigned priorities 
    (either strings or integers), and the task list can be customized or sorted based on these priorities.

    Attributes:
        to_do (dict): Dictionary of tasks yet to be completed, with task names as keys and their priorities as values.
        done (dict): Dictionary of tasks that have been completed, with task names as keys and their priorities as values.
        daily_added_tasks (dict): Dictionary of tasks added during the current day, used for reporting purposes.
        daily_completed_tasks (dict): Dictionary of tasks completed during the current day, used for reporting purposes.
        priority_levels (list): List of acceptable priority levels, which can be strings or integers.
        default_priority (str or int): The default priority level for new tasks if none is specified.
        priorities_order_ascending (bool): Determines whether priorities are sorted in ascending order, applicable for both priorities types strings and integers.
    """
    message_theme = Theme({
        "other": "bright_cyan ",
        "info": "dim cyan italic",
        "success": "light_green bold",
        "error": "bold red"
    })
    console = Console(theme=message_theme)
    def __init__(self,
        priority_levels: List[Union[str, int]] = None,
        default_priority: Union[str, int] = 'medium',
        priorities_order_ascending: Optional[bool] =  False) -> None:

        if priority_levels is None:
            priority_levels = ['high', 'medium', 'low']

        self.priorities_type, self.default_priority = TaskManager.instantiation_legibility(priority_levels, default_priority)

        self.daily_added_tasks: Dict[str, Union[str, int]] = {}
        self.daily_completed_tasks: Dict[str, Union[str, int]] = {}
        self.to_do: Dict[str, Union[str, int]] = {}
        self.done: Dict[str, Union[str, int]] = {}
        self.priority_levels: List[Union[str, int]] = priority_levels
        self.priorities_order_ascending: bool = priorities_order_ascending

    @property
    def data(self) -> Dict[str, Dict[str, Union[str, int]]]:
        return {
            'to_do': self.to_do,
            'done': self.done,
            'daily added tasks': self.daily_added_tasks,
            'daily completed tasks': self.daily_completed_tasks
        }

    @classmethod
    def instantiation_legibility(cls, priority_levels:List[Union[str, int]], default_priority) -> Optional[Tuple[str,str]]:
        if not all(isinstance(item, type(priority_levels[0])) for item in priority_levels) :
            raise ValueError("All elements in 'priority_levels' must be of the same type.")
        priorities_type = type(priority_levels[0])

        if not isinstance(default_priority, priorities_type) or default_priority not in priority_levels:
            raise ValueError(f"Default priority must be of type {priorities_type.__name__} and in {priority_levels}.")

        if priorities_type is str:
            return "literal", default_priority
        elif priorities_type is int:
            return "numerical", default_priority
        else:
            raise ValueError("Only string and integer priority types are supported.")

    @staticmethod
    def _remove_rich_styling(text: str) -> str:
        return re.sub(r'\[.*?\]', '', text)
    
    def save_current_state(self,data_file_path: str = './data.json') -> None:
        """
        Saves the current state of the task manager to a JSON file.

        The current state includes tasks in the to-do, done, and reporting lists. The data is serialized
        and saved as a JSON file in the specified directory.

        Args:
            data_file_path (os.PathLike): The file path where the task state will be saved. Defaults to './data.json'.

        Returns:
            str: A message indicating whether the data was successfully saved, or if an error occurred.
        """

        absolute_path = os.path.abspath(data_file_path)
        directory_name = os.path.dirname(absolute_path)
        file_ext = os.path.splitext(absolute_path)[1]
        if not os.path.exists(directory_name):
            TaskManager.console.print(f"{absolute_path} is invalid as a data file path to save to.",style="error")
            return
        if file_ext.lower() != ".json":
            TaskManager.console.print(f"{data_file_path} is invalid as a data file to save to, only \".json\" files allowed.", style="error")
            return

        with open(data_file_path, 'w') as data_safe:
            json.dump(self.data, data_safe, indent=2)
        TaskManager.console.print(f"Data written successfully at \"{os.path.abspath(data_file_path)}\" .",style="success")
    
    def load_state(self,data_file_path: Optional[str] = './data.json') -> None:
        """
        Loads a task manager state from a JSON file.

        This method retrieves and loads the saved task state from the specified JSON file. If the file 
        does not exist or contains invalid data, the state will be reset and a fresh start initiated.

        Args:
            data_file_path (str, optional): The file path from which to load the state. Defaults to './data.json'.

        Returns:
            str: A message indicating whether the data was successfully loaded or if an error occurred.
        """

        if not os.path.exists(data_file_path):
            self.clear()
            TaskManager.console.print(f"\"{data_file_path}\" Doesn't exist. Starting fresh.",style="info")

        try:
            with open(data_file_path, 'r') as data_safe:
                data = json.load(data_safe)
            self.to_do = data.get('to_do', {})
            self.done = data.get('done', {})
            self.daily_added_tasks = data.get('daily added tasks', {})
            self.daily_completed_tasks = data.get('daily completed tasks', {})

            TaskManager.console.print("Data loaded successfully, ready to go!",style="info")
        except FileNotFoundError:
            self.clear()
            TaskManager.console.print('No saved data found, starting fresh.',style="error")  
        except JSONDecodeError as e:
            TaskManager.console.print(f"Error parsing JSON: {e}\nStarting Fresh.",style="error")
            self.clear()      

    def _verify_task_priority(self,task_priority:Union[str,int], which_one:Literal['task','priority']):
        if which_one == 'priority':
            types_reference = {
                str:"literal",
                int:"numerical"
            }
            expected_type = self.priorities_type
            actual_type = type(task_priority)
            actual_label = types_reference.get(actual_type, "unknown")
            if actual_label == expected_type:
                return task_priority
            else:
                raise ValueError(f"Invalid priority type: expected a {expected_type} , but received a {actual_label} ({actual_type.__name__}).")
        elif which_one == 'task':
            if type(task_priority) is not str:
                raise ValueError(f"Invalid task type: expected a string, but received a value of type {type(task_priority).__name__} ({task_priority}).")
            else:
                return task_priority

    def add_task(self, *tasks_priorities: Union[str, Tuple[str, Union[str, int]]]) -> str:  
        """
        Adds one or more tasks to the to-do list if they are not already present.

        Args:
            *tasks_priorities: The tasks to be added to the to-do list. Can be a string (task name) or a tuple (task name, priority).

        Returns:
            str: A message indicating which tasks were added, not added or already exist in the list.
        """
        added_tasks = []
        not_added = []
        not_added_existence = []
        not_added_priority = []
        lowercase_tasks = {task.lower() for task in self.to_do}
        lowercase_priority_levels = {p.lower() for p in self.priority_levels} if self.priorities_type == "literal" else set(self.priority_levels)
        for tasks in tasks_priorities:
            if isinstance(tasks, tuple) and len(tasks) == 2:
                task, priority = self._verify_task_priority(tasks[0], which_one='task'), self._verify_task_priority(tasks[1], which_one='priority')
            elif isinstance(tasks, str):
                task, priority = tasks, self.default_priority
            else:
                TaskManager.console.print(f"{tasks} can't be added.",style="error")
                continue
            lowercase_task = task.lower()
            lowercase_priority = priority.lower()
            if self.priorities_type == "literal":
                if lowercase_task not in lowercase_tasks and lowercase_priority in lowercase_priority_levels:
                    self.to_do[task] = priority
                    self.daily_added_tasks[task] = priority
                    added_tasks.append(f"{task} [bright_blue i](Priority: {priority})[/bright_blue i]") 
                elif lowercase_task in lowercase_tasks and lowercase_priority not in lowercase_priority_levels:
                    not_added.append(task)
                elif lowercase_task in lowercase_tasks:
                    not_added_existence.append(task)
                elif lowercase_priority not in lowercase_priority_levels:
                    not_added_priority.append(f'{task} [bright_blue i](Priority: {priority})[/bright_blue i]')
            elif self.priorities_type == "numerical":
                if lowercase_task not in lowercase_tasks and priority in self.priority_levels:
                    self.to_do[task] = priority
                    self.daily_added_tasks[task] = priority
                    added_tasks.append(f"{task} [bright_blue i](Priority: {priority})[/bright_blue i]") 
                elif lowercase_task in lowercase_tasks and priority not in self.priority_levels:
                    not_added.append(task)
                elif lowercase_task in lowercase_tasks:
                    not_added_existence.append(task)
                elif priority not in self.priority_levels:
                    not_added_priority.append(f'{task} [bright_blue i](Priority: {priority})[/bright_blue i]')

        response = []
        if added_tasks:
            if len(added_tasks) == 1:
                response.append(f"[success]{',\n'.join(added_tasks)}[/success] [info]added successfully.[/info]\n")
            else:
                response.append(f"[success]{',\n'.join(added_tasks)}[/success] [info]added successfully.[/info]\n")
        if not_added:
            if len(not_added) == 1:
                response.append(f"[error]{',\n'.join(not_added)}[/error] [info]wasn't added to the To-Do list.[/info]\n ")
            else:
                response.append(f"[error]{',\n'.join(not_added)}[/error] [info]weren't added to the To-Do list.[/info]\n ")
        if not_added_existence:
            if len(not_added_existence) == 1:
                response.append(f"[info]{',\n'.join(not_added_existence)}[/info] is already in the To-Do list:\n{self.current_state('to-do')}")
            else:
                response.append(f"[info]{',\n'.join(not_added_existence)}[/info] are already in the To-Do list:\n{self.current_state('to-do')}")
        if not_added_priority:
            if len(not_added_priority) == 1:
                response.append(f"[error]{',\n'.join(not_added_priority)}[error] has an invalid priority. Available priorities are:\n{"; ".join(self.priority_levels)}")
            else:
                response.append(f"[error]{',\n'.join(not_added_priority)}[error] have an invalid priority. Available priorities are:\n{"; ".join(self.priority_levels)}")
        TaskManager.console.print(" ".join(response))
        return self._remove_rich_styling(" ".join(response))

    def remove_task(self,*tasks: str) -> None:
        """
        Removes one or more tasks from the to-do list.

        Args:
            *tasks: One or more tasks to remove from the to-do list.

        Returns:
            A message indicating whether the tasks were removed successfully.
        """
        removed_tasks = []
        not_found_tasks = []
        task_keys = {task.lower(): task for task in self.to_do.keys()}
        for task in tasks:
            if task.lower() in task_keys:
                og_task = task_keys[task.lower()]
                self.to_do.pop(og_task)
                self.daily_added_tasks.pop(og_task)
                removed_tasks.append(og_task)
            else:
                not_found_tasks.append(task)

        if removed_tasks and not_found_tasks:
            TaskManager.console.print(f"[success]{', '.join(removed_tasks)} removed successfully.[/success]\n[error]However, {', '.join(not_found_tasks)} not found in the to-do list.[/error]")
        elif removed_tasks:
            TaskManager.console.print(f"[success]{', '.join(removed_tasks)} removed successfully.[/success]")
        elif not_found_tasks:
            TaskManager.console.print(f"[error]{', '.join(not_found_tasks)} not found in the to-do list.[/error]")

    def task_done(self, *tasks: str) -> None:
        """
        Marks one or more tasks as done by moving them from the to-do list to the done list.

        Tasks are moved from the to-do list to the done list. If a task is already in the done list, it will 
        not be marked again.

        Args:
            *tasks (str): The task names to be marked as done.

        Returns:
            str: A message indicating which tasks were successfully marked as done, already completed, or not found.
        """

        done_tasks = []
        already_done_tasks = []
        absent_tasks = []
        task_keys = {task.lower(): task for task in self.to_do.keys()}
        for task in tasks:
            if task.lower() in task_keys:  
                original_task = task_keys[task.lower()]  
                if original_task not in self.done:  
                    self.done[original_task] = self.to_do[original_task]  
                    self.daily_completed_tasks[original_task] = self.to_do[original_task]  
                    self.to_do.pop(original_task)  
                    done_tasks.append(original_task)  
                else:
                    already_done_tasks.append(original_task) 
            else:
                absent_tasks.append(task)  
        response = []
        if done_tasks:
            response.append(f"[success]{',\n'.join(done_tasks)}[success] [info]marked as done.\n[/info]")
        if already_done_tasks:
            response.append(f"[info]{',\n'.join(already_done_tasks)} already done.[/info]")
        if absent_tasks:
            response.append(f"[error]{',\n'.join(absent_tasks)} not in to-do list.[/error]")
        TaskManager.console.print((" ".join(response)))

    def _format_task_list(self, tasks: Dict[str, Union[str, int]], which_one: str, print_it : bool = True) -> str :
        """
        Formats a dictionary of tasks for display, numbering them and displaying their priority levels.

        The tasks are sorted by their priority levels and formatted into a numbered list for easier reading.

        Args:
            tasks (dict): Dictionary of tasks with task names as keys and priorities as values.
            which_one (str): Specifies whether the tasks are 'to-do' or 'done' for labeling purposes.

        Returns:
            str: A formatted string of tasks, including numbering and priority levels.
        """

        if not tasks:
            return f"No {which_one} tasks."
        
        if self.priorities_type == "numerical":
            sorted_tasks = sorted(tasks.items(), key=lambda x : self.priority_levels.index(x[1]), reverse=self.priorities_order_ascending)
        elif self.priorities_type == "literal":
            sorted_tasks = sorted(tasks.items(), key=lambda x: self.priority_levels.index(x[1].lower()), reverse=self.priorities_order_ascending)
        if print_it:
            tasks_table = Table(title=which_one.title())
            tasks_table.add_column("Task") 
            tasks_table.add_column("Priority")

            for task, priority in sorted_tasks:
                tasks_table.add_row(task.capitalize(), str(priority))

            TaskManager.console.print(tasks_table)

        # To save the text report:
        
        max_task_length = max(len(task) for task in tasks.keys()) + 2
        header = f"{'ID':<4} {'Task':<{max_task_length}} Priority\n{'-'*4} {'-'*max_task_length} {'-'*8}\n"
        formatted_list = f"{which_one.capitalize()} Tasks:\n"
        formatted_list += header
        if self.priorities_type == "literal":
            for idx, (task,priority) in enumerate(sorted_tasks, 1):
                formatted_list += f"{idx:<5}{task:<{max_task_length+1}}{priority.capitalize()}\n"
            return formatted_list
        elif self.priorities_type == "numerical":
            for idx, (task,priority) in enumerate(sorted_tasks, 1):
                formatted_list += f"{idx:<5}{task:<{max_task_length+1}}{priority}\n"
            return formatted_list  

    def report(self, file_path: str = './', report_name: str = f"{date.today()}_tasks.txt",report_content: Literal['all', 'todo', 'done'] = 'all') :
        """
        Generates and saves a report of the day's to-do and completed tasks to a text file.

        The report can include either to-do tasks, done tasks, or both. It is saved to the specified file path.

        Args:
            file_path (str, optional): The directory where the report will be saved. Defaults to './' (The cwd).
            report_name (str, optional): The name of the file where the report will be saved. Defaults to a file named with the current date.
            report_content (str, optional): Specifies which tasks to include in the report ('todo', 'done', or 'all'). Defaults to 'all'.

        Returns:
            str: A message confirming the report was saved, or an error message if no tasks were found.
        """
        def _finalize():
            file_name = os.path.abspath(os.path.join(file_path, report_name))
            with open(file_name, 'w') as report_file:
                report_file.write(report)
            TaskManager.console.print(f"[success]Report successfully generated and saved as \"{file_name}\"[/success]")

        if not self.daily_added_tasks and not self.daily_completed_tasks:
            TaskManager.console.print("Both lists are empty, are you willing to save nothing? Do something, you Panda.",style="info")
        else:
            todo_final = self._format_task_list(self.daily_added_tasks, 'To-Do', print_it=False)
            done_final = self._format_task_list(self.daily_completed_tasks, 'Done', print_it=False)
            if report_content.lower() == 'todo': 
                report = f'''{date.today()} Tasks were:

{todo_final}        
            '''
                _finalize()

            elif report_content == 'done':
                report = f'''{date.today()} Tasks were:

{done_final}        
            '''
                _finalize()

            else:
                report = f'''{date.today()} Tasks were:

{todo_final}

{done_final}
            '''
                _finalize()
                
    def current_state(self, option: Literal['both', 'to-do', 'done'] = 'both', print_it:bool = True) -> None:
        """ 
        Displays the current state of the task manager, showing either the to-do, done, or both lists.

        Args:
            option (str, optional): The task list(s) to display ('to-do', 'done', or 'both'). Defaults to 'both'.
            print_it (bool): Whether the current state gets printed or not.

        Returns:
            str: A formatted string representing the requested task list(s).
        """
        if option == 'both':
            self._format_task_list(self.to_do, 'to-do', print_it)
            self._format_task_list(self.to_do, 'done', print_it)
        elif option == 'to-do':
            self._format_task_list(self.to_do, 'to-do', print_it)
        elif option == 'done':
            self._format_task_list(self.done, 'done', print_it)
        else:
            TaskManager.console.print("Invalid option.",style="error")

    def clear(self,which_one:  Literal['both','todo','done'] = 'both') -> None:
        """
        Resets todo list or done list or both lists.

        Returns:
            str: A message indicating whether specified list was cleared successfully.
        """
        if which_one.lower() == 'todo':
            if self.to_do:
                self.to_do.clear()
                self.daily_added_tasks.clear()
                TaskManager.console.print(" To-do list is cleared successfully.",style="success")
            else:
                TaskManager.console.print("To-do list is empty.",style="info")
        elif which_one.lower() == 'done': 
            if self.done:
                self.done.clear()
                self.daily_completed_tasks.clear()
                TaskManager.console.print("Done list is cleared successfully.",style="success")
            else:
                TaskManager.console.print("Done list is empty.",style="info")
        elif which_one.lower() == 'all': 
            if self.to_do:
                self.to_do.clear()
                self.daily_added_tasks.clear()
                self.done.clear()
                self.daily_completed_tasks.clear()
                TaskManager.console.print("Both lists are cleared successfully.",style="success")
            else:
                TaskManager.console.print("Both lists are empty.None cleared.",style="info")
        else:
            TaskManager.console.print("Invalid option.",style="error")

    def __str__(self):
        to_do_state = self._format_task_list(self.to_do, 'to-do', print_it=False)
        done_state = self._format_task_list(self.done, 'done', print_it=False)
        return f"Task Manger Current state:\n\n{to_do_state}\n\n{done_state}"
