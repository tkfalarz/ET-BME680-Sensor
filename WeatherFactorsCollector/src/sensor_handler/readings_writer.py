import pathlib
from datetime import datetime


class ReadingsWriter:
    def __init__(self):
        readings_filename = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.txt"
        readings_dir_path = pathlib.Path(f"{pathlib.Path(__file__).parent.parent}/readings")

        self.__absolute_file_path = self.__try_create_file(readings_dir_path, readings_filename)

    def save_to_file(self, readings: str):
        with open(self.__absolute_file_path, "a") as readings_file:
            readings_file.write(readings)

    @staticmethod
    def __try_create_file(readings_dir_path: pathlib.Path, readings_filename: str) -> str:
        if not readings_dir_path.exists():
            readings_dir_path.mkdir()

        readings_file_path = readings_dir_path.joinpath(readings_filename)
        if not readings_file_path.exists():
            readings_file_path.touch()

        return f"{readings_file_path}"
