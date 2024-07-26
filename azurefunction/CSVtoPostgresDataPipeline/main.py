from download_file import download_file
from fill_database import fill_database
import pathlib

download_file()
fill_database()
pathlib.Path("test.csv").unlink()