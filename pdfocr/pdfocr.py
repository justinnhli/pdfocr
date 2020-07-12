#!/usr/bin/env python3

from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from pytesseract import image_to_string
from PIL import Image


def ocr_directory(path, verbose=False):
    # type: (Path, bool) -> str
    """Convert a directory of images to text."""
    # TODO deal with other image formats
    image_paths = sorted(path.glob('page*.png'))
    result = []
    for index, image_path in enumerate(image_paths, start=1):
        if verbose:
            print(f'processing page {index} of {len(image_paths)}')
        result.append(ocr_image_file(image_path))
    return '\n'.join(result)


def ocr_image_file(path, verbose=False):
    # type: (Path, bool) -> str
    """Convert an image to text."""
    return image_to_string(Image.open(str(path)))


def ocr_pdf_file(path, verbose=False):
    # type: (Path, bool) -> str
    """Convert an PDF file to text."""
    with TemporaryDirectory() as temp_dir:
        run(
            [
                'gs',
                '-q',
                '-dQUIET',
                '-dPARANOIDSAFER',
                '-dBATCH',
                '-dNOPAUSE',
                '-dNOPROMPT',
                '-sDEVICE=png16m',
                '-dTextAlphaBits=4',
                '-dGraphicsAlphaBits=4',
                '-r300x300',
                '-sOutputFile="page%03d.png"',
                str(path),
            ],
            cwd=temp_dir,
            check=True,
        )
        return ocr_directory(Path(temp_dir))
