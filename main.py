# main.py

# Direct Commits: Commits made directly to the main branch will be captured as they have a single parent.
# Squashed Commits: When commits are squashed and merged, they will also appear as single-parent commits and will be included in the analysis.
# Rebase and Merge Commits: After rebase and merge, the rebased commits will appear as if they were made directly on top of the main branch, each having a single parent.
# Merge Commits: Merge commits that integrate changes from one branch into another and have multiple parents will be ignored to avoid double-counting.






from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from datetime import datetime, timedelta
import os
from src.generate_report import generate_report
from config import REPO_OWNER, REPO_NAME, ACCESS_TOKEN

app = FastAPI()

# API call for generating report
# With custom date range:      http://localhost:8000/generate_report?start_date=01-06-24&end_date=20-06-24

# Default to the last 7 days:  http://localhost:8000/generate_report

@app.get("/generate_report")
def generate_report_endpoint(start_date_str: Optional[str] = Query(None), end_date_str: Optional[str] = Query(None)):
    #date format is  dd-mm-yy
    date_format = "%d-%m-%y"
    
    try:
        # if start and end date are specified
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format)
        # if start and end date are not specified we take end date as the current date and start date as (end date - 7 days) weekly report
        else:
            end_date = datetime.now(UTC)
            start_date = end_date - timedelta(days=60)
        # if both start and end date are invalid(i.e. dates are greater than today's date)
        if start_date > datetime.now(UTC) and end_date > datetime.now(UTC):
            print("Both Start and End Dates are invalid")
            raise HTTPException(status_code=400, detail="Both Start and End Dates are invalid")
        # if start date is greater than today's date
        if start_date > datetime.now(UTC):
            print("Start Date is invalid")
            raise HTTPException(status_code=400, detail="Start Date is invalid")
        # if end date is greater than today's date
        if end_date > datetime.now(UTC):
            print("End Date is invalid")
            raise HTTPException(status_code=400, detail="End Date is invalid")
        # if end date is smaller than start date raise exception
        if end_date < start_date:
            print("End date must be greater than start date.")
            raise HTTPException(status_code=400, detail="End date must be greater than start date.")

    # if dates are not in valid format
    except ValueError:
        print("Incorrect date format, should be dd-mm-yy.")
        raise HTTPException(status_code=400, detail="Incorrect date format, should be dd-mm-yy.")

    print("Generating report...")
    # generating report
    file_path = generate_report(REPO_OWNER, REPO_NAME, ACCESS_TOKEN, start_date, end_date)
    print(f"Report Generated for {start_date} to {end_date}")
    return {"message": "Report generated", "file_path": file_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
