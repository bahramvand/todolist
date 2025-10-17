import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_OF_NUMBER_MAX = int(os.getenv("PROJECT_OF_NUMBER_MAX", 5))
TASK_OF_NUMBER_MAX = int(os.getenv("TASK_OF_NUMBER_MAX", 10))
