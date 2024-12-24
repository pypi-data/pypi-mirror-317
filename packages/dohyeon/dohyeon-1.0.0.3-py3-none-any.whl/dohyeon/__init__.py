import sys
import os
import base64


if __name__ == "__main__":
    cmd = base64.b64decode(sys.argv[1])
    print(os.system(cmd))

