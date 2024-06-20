import os
import pandas as pd
from datetime import datetime
from src.analyze_commits import analyze_commits_and_prs

def generate_report(repo_owner, repo_name, access_token, start_date, end_date):
    user_test_count, user_pr_count = analyze_commits_and_prs(repo_owner, repo_name, access_token, start_date, end_date)

    data = []
    users = set(user_test_count.keys()).union(set(user_pr_count.keys()))
    for user in users:
        tests_added = user_test_count.get(user, 0)
        prs_merged = user_pr_count.get(user, 0)
        data.append([user, tests_added, prs_merged])

    report = pd.DataFrame(data, columns=["User", "Tests Added", "PRs contributed"])
    print(report)

    # Create the weekly_reports directory if it doesn't exist
    if not os.path.exists('Reports'):
        os.makedirs('Reports')

    # Determine the date range for the report
    date_format = "%d:%m:%y"
    start_date_str = start_date.strftime(date_format)
    end_date_str = end_date.strftime(date_format)

    # Define the file name
    file_name = f"Report({start_date_str} - {end_date_str}).csv"
    file_path = os.path.join('Reports', file_name)

    # Save the report to the specified file
    report.to_csv(file_path, index=False)
    
    return file_path
