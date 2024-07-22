from src.download_file import download_file
from src.fill_database import fill_database
import pathlib

def main():
    download_file()
    fill_database()
    pathlib.Path("data/test.csv").unlink()
    
if __name__ == "__main__":
    main()