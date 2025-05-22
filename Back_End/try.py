import systemfnc as fnc

def main():
    dummylogdata = """
    name: test
    password: test
    email: test
    """
    fnc.Sys_log("test", dummylogdata).write_log()
    
if __name__ == "__main__":
    main()