# utils/content_utils.py

import base64
import re
import requests
#getting file content for a given commit_sha
def get_file_content_at_commit(file_path, commit_sha, repo_owner, repo_name, access_token):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref={commit_sha}'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = base64.b64decode(response.json()['content'])
        return content.decode('utf-8')
    return None
#rule for counting the number of "test(" occurences in a given file 
def count_tests_in_content(content):
    return len(re.findall(r'test\(', content))
