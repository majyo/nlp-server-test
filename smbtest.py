import logging
from smb.SMBConnection import SMBConnection


if __name__ == "__main__":
    connection = SMBConnection("robin", "smb@123", "", "", use_ntlm_v2=True)
    result = connection.connect("192.168.40.10", 445)
    print(result)