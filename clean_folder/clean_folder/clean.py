import re
import argparse
import shutil
from pathlib import Path
from shutil import copyfile

CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANSLIT_DICT = {}

for c, l in zip(CYRILLIC, LATIN):
    TRANSLIT_DICT[ord(c)] = l
    TRANSLIT_DICT[ord(c.upper())] = l.upper()

def normalize(text):
    rep = re.compile("[^a-zA-Zа-яА-я\d]")
    text_without_symbol = rep.sub("_", text)

    normalize_text = text_without_symbol.translate(TRANSLIT_DICT)
    return normalize_text


parser = argparse.ArgumentParser(description='Sorting directory')
parser.add_argument('--source', '-s', required=True, help='Source folser')

args = vars(parser.parse_args())
source = args.get('source')


def sort_folder(path: Path):
    for element in path.iterdir():
        if element.is_dir():
            sort_folder(element)
        else:
            extension = element.suffix
            new_name = normalize(element.stem)+extension
            if extension == '.jpeg' or extension == '.png' or extension == '.jpg' or extension == '.sng':
                new_path = output_folder / 'images'
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(element, new_path / new_name)
            elif extension == extension == '.avi' or extension == '.mp4' or extension == '.mov' or extension == '.mkv':
                new_path = output_folder / 'video'
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(element, new_path / new_name)
            elif extension == '.DOC' or extension == '.docx' or extension == '.txt' or extension == '.pdf' or extension == '.xlsx' or extension == '.pptx':
                new_path = output_folder / 'documents'
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(element, new_path / new_name)
            elif extension == '.MP3' or extension == '.ogg' or extension == '.wav' or extension == '.amr':
                new_path = output_folder / 'audio'
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(element, new_path / new_name)
            elif extension == extension == '.zip' or extension == '.gz' or extension == '.tar':
                new_path = output_folder / 'archives' / new_name
                shutil.unpack_archive(element, new_path)
            else:
                new_path = output_folder / 'others'
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(element, new_path / new_name)


output_folder = Path(source)
sort_folder(Path(source))
