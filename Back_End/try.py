import systemfnc as fnc

def main():
    data = fnc.database_con().read("accounts", "*")
    for row in data:
        print(row[5])
        decode = fnc.Security().decrypt_str(row[5])
        print(decode)

    
if __name__ == "__main__":
    main()