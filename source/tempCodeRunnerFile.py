    username = getpass.getuser()
    domain = os.getenv("USERDOMAIN")
    
    # In case of no domain assume we are at home
    if isinstance(domain,type(None)):
        domain = "Home"
    
    print(
        f"{username} @ {domain}"
    )
    print(">",end="")