import requests

def login(username, password):
    login_url = "https://myqlik.qlik.com/tenants/login"
    session = requests.Session()

    # Send a POST request to the login URL with the credentials
    response = session.post(login_url, data={"username": username, "password": password})
    print(response)

    # Check if the login was successful
    if response.status_code == 200:
        print(session)
        return session
    else:
        print("Login failed. Please check your credentials.")
        return None

def get_reports(session):
    reports_url = "https://myqlik.qlik.com/reports"  # URL for retrieving reports

    # Send a GET request to the reports URL using the authenticated session
    response = session.get(reports_url)

    # Check if the request was successful
    if response.status_code == 200:
        reports = response.json()  # Assuming the response is in JSON format
        return reports
    else:
        print("Failed to retrieve reports.")
        return None

# Enter your Qlik Cloud credentials
username = "akadhr@maqsoftware.com"
password = "End@world!32"

# Log in to Qlik Cloud
session = login(username, password)

# Check if login was successful
if session:
    # Retrieve the reports
    reports = get_reports(session)
    print(reports)

    # Print the reports
    if reports:
        print("Reports:")
        for report in reports:
            print(report["name"])
    else:
        print("No reports found.")
else:
    print("Login unsuccessful.")
