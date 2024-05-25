from json import dumps

from requests import post


def _fetch_user_data() -> dict:
    leetcode_url: str = 'https://leetcode.com/graphql'
    headers: dict[str, str] = {
        'Content-Type': 'application/json'
    }
    graphql_query: str = '''
        {
            matchedUser(username: 'twrskshm') {
                submitStats: submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                }
            }
        }
    '''
    payload: str = dumps(
        {
            'query': graphql_query
        }
    )
    leetcode_response: dict = post(leetcode_url, headers=headers, data=payload).json()

    return leetcode_response['data']['matchedUser']


def generate_markdown() -> str:
    user_data: dict = _fetch_user_data()
    submissions: dict = user_data['submitStats']['acSubmissionNum']
    count_key: str = 'count'
    total_solved: str = submissions[0][count_key]
    easy_solved: str = submissions[1][count_key]
    medium_solved: str = submissions[2][count_key]
    hard_solved: str = submissions[3][count_key]

    markdown = f'''
## LeetCode
- **Total Problems Solved**: {total_solved}
    - Easy: {easy_solved}
    - Medium: {medium_solved}
    - Hard: {hard_solved}
    '''

    return markdown
