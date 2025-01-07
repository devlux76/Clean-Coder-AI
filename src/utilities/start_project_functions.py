"""
Functions called when new project is initialized.
"""

import os
from src.utilities.user_input import user_input
from src.utilities.print_formatters import print_formatted


def create_coderignore(work_dir):
    coderignore_path = os.path.join(work_dir, '.clean_coder', '.coderignore')
    default_ignore_content = ".env\n.git/\n.idea/\n.clean_coder/\n.coderrules\n.vscode\n.gitignore\nnode_modules/\nvenv/\nenv/\n __pycache__\n*.pyc\n*.log"
    os.makedirs(os.path.dirname(coderignore_path), exist_ok=True)
    if not os.path.exists(coderignore_path):
        with open(coderignore_path, 'w', encoding='utf-8') as file:
            file.write(default_ignore_content)
        print_formatted(".coderignore file created successfully.", color="green")


def create_project_plan_file(work_dir):
    project_plan_path = os.path.normpath(os.path.join(work_dir, '.clean_coder', 'project_plan.txt'))
    project_plan = user_input("Describe what needed to be done in your project in as much detail as possible. ")
    with open(project_plan_path, 'w', encoding='utf-8') as file:
        file.write(project_plan)
    print_formatted(f"Project plan saved. You can edit it in {project_plan_path}.", color="green")
    return project_plan


def set_up_dot_clean_coder_dir(work_dir):
    create_coderignore(work_dir)
