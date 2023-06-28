
## setting up the Qlik CLI and accessing the list of apps present in it

import subprocess
import sys

def main(context_name ,qlik_tenant_url, api_key):
    # context_name = input("Enter Context Name : ")
    # set1 = subprocess.run(["qlik", "context", "init"] + [context_name])
    # result = subprocess.run('qlik app ls', capture_output=True, text=True)
    # print(result)

    print("Context Name:", context_name)
    print("Qlik Tenant URL:", qlik_tenant_url)
    print("API Key:", api_key)

    ## setting
    subprocess.run(["qlik", "context", "create"] + [context_name] + ["--api-key"] + [api_key] + ["--server"] + [qlik_tenant_url], capture_output=True, text=True)
    # print(set1)
    set2 = subprocess.run(["qlik", "context", "use"] + [context_name])
    # print(set2)

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
    context_name_arg = arguments[2].strip()
    qlik_tenant_url_arg = arguments[3].strip()
    api_key_arg = arguments[4].strip()
    try:
        print("Get List Started")
        main(context_name_arg, qlik_tenant_url_arg, api_key_arg)
        print("Get List Stopped")
    except:
        print("Get List Trigger Failed")


