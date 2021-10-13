
def authenticateUser(auth):
    print(auth)
    if auth == "my-token":
        return True
    else:
        return False
