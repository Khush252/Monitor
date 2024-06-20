from utils.content_utils import get_file_content_at_commit, count_tests_in_content
from utils.github_api import fetch_commit_details, fetch_commits_from_github, fetch_closed_prs, filter_merged_prs, fetch_commits_in_pr

# given commit's sha get author and then check if files that end with .test.ts have any changes
# i.e. first get prev content and current content then count the number of "test(" , subtract to get ans
def analyze_commit(commit_sha, repo_owner, repo_name, access_token):
    commit_data = fetch_commit_details(commit_sha, repo_owner, repo_name, access_token)

    author = commit_data['commit']['author']['name']
    files = commit_data['files']
    test_count_change = 0

    for file in files:
        if file['filename'].endswith(".test.ts"):
            file_path = file['filename']
            previous_content = get_file_content_at_commit(file_path, commit_data['parents'][0]['sha'], repo_owner, repo_name, access_token)
            current_content = get_file_content_at_commit(file_path, commit_sha, repo_owner, repo_name, access_token)

            if previous_content and current_content:
                previous_test_count = count_tests_in_content(previous_content)
                current_test_count = count_tests_in_content(current_content)
                test_count_change += current_test_count - previous_test_count

    return author, test_count_change


def analyze_commits_and_prs(repo_owner, repo_name, access_token, start_date, end_date):
    all_commits = fetch_commits_from_github(repo_owner, repo_name, access_token, start_date, end_date)
    user_test_count = {}
    user_pr_count = {}
    
    for commit in all_commits:
        if len(commit['parents']) == 1:
            author, test_count_change = analyze_commit(commit['sha'], repo_owner, repo_name, access_token)

            if author in user_test_count:
                user_test_count[author] += test_count_change
            else:
                user_test_count[author] = test_count_change

    all_prs = fetch_closed_prs(repo_owner, repo_name, access_token, start_date, end_date)
    merged_prs = filter_merged_prs(all_prs, start_date, end_date)

    for pr in merged_prs:
        pr_number = pr['number']
        commits_in_pr = fetch_commits_in_pr(repo_owner, repo_name, pr_number, access_token)
        unique_authors = set()

        for commit in commits_in_pr:
            commit_author = commit['commit']['author']['name']
            unique_authors.add(commit_author)

        for author in unique_authors:
            if author in user_pr_count:
                user_pr_count[author] += 1
            else:
                user_pr_count[author] = 1

    return user_test_count, user_pr_count
