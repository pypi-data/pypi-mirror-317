import os
import os
import re
import subprocess

from ok import Logger
from ok.update.python_env import delete_files, \
    create_venv

logger = Logger.get_logger(__name__)


def replace_string_in_file(file_path, old_pattern, new_string):
    """
    Replace occurrences of old_pattern with new_string in the specified file using regex.

    :param file_path: Path to the file
    :param old_pattern: Regex pattern to be replaced
    :param new_string: Replacement string
    """

    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace the old pattern with the new string using regex
    new_content = re.sub(old_pattern, new_string, content)

    # Write the new content back to the file
    with open(file_path, 'w') as file:
        file.write(new_content)

    logger.info(f"Replaced pattern '{old_pattern}' with '{new_string}' in {file_path}")


def create_repo_venv(python_dir, code_dir='.', last_env_folder=None, index_url="https://pypi.org/simple/"):
    logger.info(f'create_repo_venv: {python_dir} {code_dir} {last_env_folder} {index_url}')
    lenv_path = create_venv(python_dir, code_dir, last_env_folder)
    # return
    try:
        pip_exe = os.path.join(lenv_path, 'Scripts', 'pip')
        if not os.path.isabs(pip_exe):
            pip_exe = os.path.abspath(pip_exe)
        params_install = [pip_exe, "install", "pip-tools", "-i", index_url, '--no-cache']
        print(f"Running command: {' '.join(params_install)}")
        result_install = subprocess.run(params_install, check=True, cwd=code_dir, capture_output=True, encoding='utf-8',
                                        text=True)

        print("\n--- pip install pip-tools Output ---")
        print("Standard Output:")
        print(result_install.stdout)
        print("Standard Error:")
        print(result_install.stderr)

        # Run pip-sync
        pip_sync = os.path.join(lenv_path, 'Scripts', 'pip-sync')
        if not os.path.isabs(pip_sync):
            pip_sync = os.path.abspath(pip_sync)
        python_executable = os.path.join(lenv_path, 'Scripts', 'python')
        if not os.path.isabs(python_executable):
            python_executable = os.path.abspath(python_executable)
        requirements = os.path.join(code_dir, 'requirements.txt')
        if not os.path.isabs(requirements):
            requirements = os.path.abspath(requirements)
        params_sync = [pip_sync, requirements, '--python-executable', python_executable, "-i", index_url, '--pip-args',
                       '"--no-cache"']
        print(f"\nRunning command: {' '.join(params_sync)}")
        result_sync = subprocess.run(params_sync, check=True, cwd=code_dir, capture_output=True, encoding='utf-8',
                                     text=True)

        print("\n--- pip-sync Output ---")
        print("Standard Output:")
        print(result_sync.stdout)
        print("Standard Error:")
        print(result_sync.stderr)
        logger.info("sync requirements success")
        if not last_env_folder:
            delete_files(root_dir=python_dir)
            delete_files(root_dir=lenv_path)
        return True
    except Exception as e:
        logger.error("An error occurred while creating the virtual environment.", e)
