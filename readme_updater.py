from datascraper.leetcode.leetcode_scraper import generate_markdown


def update_readme():
    leetcode_section = generate_markdown()

    with open('README.md', 'r') as readme_file:
        readme_content = readme_file.readlines()

    # Find the LeetCode section and update it.
    start_line = None
    end_line = None

    for line_index, line in enumerate(readme_content):
        if line.strip() == '## LeetCode':
            start_line = line_index
        elif start_line is not None and line.startswith('## ') and line.strip() != '## LeetCode':
            end_line = line_index
            break

    if start_line is not None:
        if end_line is None:
            end_line = len(readme_content)

        readme_content = (
            readme_content[:start_line - 1] +
            leetcode_section.splitlines(keepends=True) +
            readme_content[end_line:]
        )
    else:
        # Append if LeetCode section not found.
        readme_content.append(leetcode_section)

    with open('README.md', 'w') as readme_file:
        readme_file.writelines(readme_content)


if __name__ == '__main__':
    update_readme()
