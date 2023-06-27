
import subprocess
def main():
    print("main called")
    # x = input("enter name : ")
    # print(x)
    result = subprocess.run('qlik app ls', capture_output=True, text=True)

    print(result)


if __name__ == '__main__':
    print("start")
    # x = input("enter name : ")
    # print(x)
    main()
