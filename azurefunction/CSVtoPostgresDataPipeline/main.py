from src.download_file import download_file
from src.fill_database import fill_database
import pathlib

download_file()
fill_database()
pathlib.Path("data/test.csv").unlink()