def GetInfoMsg():
    infoMsg = "This python snippet is triggered by the 'cmd' property.\r\n"
    infoMsg += "Any command line may be triggered with the 'cmd' property.\r\n"
    return infoMsg

if __name__ == "__main__":
    print(GetInfoMsg())