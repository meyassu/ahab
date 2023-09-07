import subprocess

SRC = "detect.py"
WGTS_PATH = "../model/best.pt"
TEST_DATA_PATH = "../data/images/test"
CONF = "0.5"
JOB_NAME = "akl"

try:
    command = [
        "python3",
        SRC,
        "--save-txt",
        "--source",
        TEST_DATA_PATH,
        "--weights",
        WGTS_PATH,
        "--conf",
        CONF,
        "--name",
        JOB_NAME
    ]
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while trying to execute the command: {e}")
