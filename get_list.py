
import subprocess
import sys

def main(qlik_tenant_url, api_key):
    # context_name = input("Enter Context Name : ")
    # set1 = subprocess.run(["qlik", "context", "init"] + [context_name])
    # result = subprocess.run('qlik app ls', capture_output=True, text=True)
    # print(result)

    print("Qlik Tenant URL:", qlik_tenant_url)
    print("API Key:", api_key)
    # Get list of apps
    cmd0 = ["qlik", "app"]
    result = subprocess.run(cmd0 + ["ls"], capture_output=True, text=True)
    rows = result.stdout.strip().split("\n")
    header = rows.pop(0)
    columns = [c.strip() for c in header.split()]
    apps = [{"ID": row.strip().split(maxsplit=1)[0], "NAME": row.strip().split(maxsplit=1)[1]} for row in rows]

    for app in apps:
        app_id = app["ID"]
        app_name = app["NAME"]
        print("App id :", app_id)
        print("App Name :", app_name)


if __name__ == '__main__':
    commandLineString = " ".join(sys.argv)
    arguments = commandLineString.split("|")
    # print("argument", arguments)
    qlik_tenant_url = arguments[2].strip()
    api_key = arguments[3].strip()
    try:
        # print("Main Trigger Started")
        main(qlik_tenant_url, api_key)
        # print("Main Triggered")
    except:
        print("Trigger Failed")


