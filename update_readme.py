from pathlib import Path
from typing import Generator
import yaml


def update_readme():
    readme_path = 'README.md'

    delete_problems_solved_section(readme_path)
    insert_problems_solved_section(readme_path)


def delete_problems_solved_section(readme_path):
    with open(readme_path, 'r') as readme_file:
        readme_contents = readme_file.readlines()

    for index, line in enumerate(readme_contents):
        if line.strip() == '## Problems Solved':
            readme_contents = readme_contents[:index]
            break

    with open(readme_path, 'w') as readme_file:
        readme_file.writelines(readme_contents)


def insert_problems_solved_section(readme_path):
    with open(readme_path, 'a') as readme_file:
        readme_file.write(f'## Problems Solved\n')

        repository_list = get_repository_list()

        for repository_name in repository_list:
            formatted_repository_name = format_directory_name(repository_name)
            problem_type_list = get_subfolder_list(repository_name)

            readme_file.write(f'### [{formatted_repository_name}](https://github.com/twrskshm/{repository_name}.git)\n')

            for problem_type in problem_type_list:
                formatted_problem_type = format_directory_name(problem_type)
                solved_problem_count = count_java_files(f'{repository_name}/{problem_type}')

                readme_file.write(f'- {formatted_problem_type}: {solved_problem_count}\n')

            readme_file.write(f'\n')


def get_repository_list():
    update_readme_path = '.github/workflows/update_readme.yml'

    with open(update_readme_path, 'r') as update_readme_file:
        update_readme_contents = yaml.safe_load(update_readme_file)

    repository_list = []
    step_list = update_readme_contents['jobs']['update-readme']['steps']

    for step in step_list:
        if step['name'] == 'Clone additional repositories':
            clone_command_list = step['run'].strip().split('\n')

            for clone_command in clone_command_list:
                if clone_command.startswith('git clone'):
                    repository_url = clone_command.split()[-1]
                    repository_name = repository_url.split('/')[-1].replace('.git', '')

                    repository_list.append(repository_name)

            break

    return repository_list


def format_directory_name(directory_name):
    words = directory_name.split('-')
    capitalized_words = [word.capitalize() for word in words]

    return ' '.join(capitalized_words)


def get_subfolder_list(directory_path):
    subdirectory_list = Path(directory_path).iterdir()

    return [
        subdirectory.name
        for subdirectory in subdirectory_list
        if subdirectory.is_dir()
        and not subdirectory.name.startswith('.')
    ]


def count_java_files(directory_path):
    java_file_paths = Path(directory_path).rglob('*.java')

    return sum(1 for _ in java_file_paths)


if __name__ == "__main__":
    update_readme()
