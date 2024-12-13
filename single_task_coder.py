"""Single coder pipeline: researcher, planner, executor and debugger."""
if __name__ == "__main__":
    from utilities.graphics import print_ascii_logo
    print_ascii_logo()
from venv import logger

from dotenv import find_dotenv

from utilities.set_up_dotenv import set_up_env_coder_pipeline

if not find_dotenv():
    set_up_env_coder_pipeline()

import os
from concurrent.futures import ThreadPoolExecutor

from agents.debugger_agent import Debugger
from agents.executor_agent import Executor
from agents.frontend_feedback import execute_screenshot_codes, write_screenshot_codes
from agents.planner_agent import planning
from agents.researcher_agent import Researcher
from utilities.print_formatters import print_formatted
from utilities.start_project_functions import set_up_dot_clean_coder_dir
from utilities.user_input import user_input
from utilities.util_functions import create_frontend_feedback_story

use_frontend_feedback = bool(os.getenv("FRONTEND_PORT"))


def run_clean_coder_pipeline(task: str, work_dir: str, docrag: str ="off") -> None:
    """Single coder pipeline run."""
    researcher = Researcher(work_dir, docrag=docrag)
    file_paths, image_paths = researcher.research_task(task)

    plan = planning(task, file_paths, image_paths, work_dir)

    executor = Executor(file_paths, work_dir)

    if use_frontend_feedback:
        create_frontend_feedback_story()
        with ThreadPoolExecutor() as executor_thread:
            future = executor_thread.submit(write_screenshot_codes, task, plan, work_dir)
            test_instruction, file_paths = executor.do_task(task, plan)
            playwright_codes, screenshot_descriptions = future.result()
        if playwright_codes:
            print_formatted("Making screenshots, please wait a while...", color="light_blue")
            first_vfeedback_screenshots_msg = execute_screenshot_codes(playwright_codes, screenshot_descriptions)
        else:
            first_vfeedback_screenshots_msg = None
    else:
        test_instruction, file_paths = executor.do_task(task, plan)
        first_vfeedback_screenshots_msg = None

    human_message = user_input("Please test app and provide commentary if debugging/additional refinement is needed.")
    if human_message in ["o", "ok"]:
        return
    debugger = Debugger(file_paths, work_dir, human_message, first_vfeedback_screenshots_msg, playwright_codes, screenshot_descriptions)
    debugger.do_task(task, plan)


if __name__ == "__main__":
    work_dir = os.getenv("WORK_DIR")
    if isinstance(work_dir, str):
        set_up_dot_clean_coder_dir(work_dir)
        task = user_input("Provide task to be executed.")
        run_clean_coder_pipeline(task, work_dir)
    else:
        logger.info("WORK_DIR environment variable is not set in .env file. Aborting.")
