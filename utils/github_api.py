import requests
from datetime import datetime

#For a paticular commit(given commit's sha) getting the details of the commit:
def fetch_commit_details(commit_sha, repo_owner, repo_name, access_token):

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# fetching all the commits within the date range from the repository
def fetch_commits_from_github(repo_owner, repo_name, access_token, start_date, end_date):
    since_str = start_date.isoformat() + 'Z'
    until_str = end_date.isoformat() + 'Z'
    
    commits_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'
    headers = {'Authorization': f'token {access_token}'}
    params = {
        'since': since_str,
        'until': until_str,
        'sha': 'main',  # Assuming main branch
    }
    response = requests.get(commits_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

#Fetching all the closed PRs from the repo
def fetch_closed_prs(repo_owner, repo_name, access_token, start_date, end_date):
    headers = {'Authorization': f'token {access_token}'}
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls'
    params = {
        'state': 'closed',
        'sort': 'updated',
        'direction': 'desc',
        'per_page': 100,
        'page': 1
    }
    all_prs = []
#handling pagination (i.e. keep true until we have no page left and store all the pages in all_prs)
    while True:
        response = requests.get(url, headers=headers, params=params)
        prs = response.json()
        if not prs:
            break
        all_prs.extend(prs)
        params['page'] += 1

    return all_prs

#getting merged PRs by using merged_at parameter which is set true if the PR is merged
def filter_merged_prs(prs, start_date, end_date):
    merged_prs = []
    for pr in prs:
        if pr['merged_at']:
            merged_at = datetime.strptime(pr['merged_at'], "%Y-%m-%dT%H:%M:%SZ")
            if start_date <= merged_at <= end_date:
                merged_prs.append(pr)
    return merged_prs

#getting all the commits for a PR (given its PR number)
def fetch_commits_in_pr(repo_owner, repo_name, pr_number, access_token):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/commits'
    headers = {'Authorization': f'token {access_token}'}
    params = {'per_page': 100, 'page': 1}
    commits = []
#handling pagination 
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        pr_commits = response.json()
        if not pr_commits:
            break
        commits.extend(pr_commits)
        params['page'] += 1

    return commits
