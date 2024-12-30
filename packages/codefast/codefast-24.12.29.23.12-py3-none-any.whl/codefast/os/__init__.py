import os


def getenv(key: str, env_file: str = '.env') -> str:
    from dotenv import load_dotenv
    load_dotenv(env_file)
    return os.getenv(key)
