import argparse
import sys
from pathlib import Path

from dslr_scan_helper.debug_context import DebugContext
from dslr_scan_helper.app import DslrScanHelperApp, DslrScanHelperContext

parser = argparse.ArgumentParser(description = 'Utility for processing film scans made with a digital camera.')
parser.add_argument('--debug', action='store_true', help='Enables extended logging.')

commands = parser.add_subparsers(help='Choose one of the following commands.', dest='command')

convert = commands.add_parser('convert', help='Converts raw files to 16bit tiff files.')
convert.add_argument('path', help='Path of file(s) to to be converted')
convert.add_argument('--bw', action='store_true', help='Enables black and white mode')


crop = commands.add_parser('crop', help='Crop images to the picture area of the negative.')
crop.add_argument('path', help='Path of file(s) to to be cropped.')

invert = commands.add_parser('invert', help='Inverts negative images.')
invert.add_argument('path', help='Path of file(s) to to be inverted.')

def files(path):
    if not path.exists():
        return [file for file in Path('.').glob(str(path)) if file.is_file()]

    if path.is_dir():
        return [file for file in path.iter_dir() if file.is_file()]

    return [path]

if __name__ == '__main__':
    args = parser.parse_args()

    context = DslrScanHelperContext()

    if args.debug:
        context = DebugContext()

    app = DslrScanHelperApp(context)

    if args.command == 'convert':
        for file in files(Path(args.path)):
            app.convert_file(file, bw=args.bw)

    if args.command == 'crop':
        for file in files(Path(args.path)):
            app.crop_file(file)

    if args.command == 'invert':
        for file in files(Path(args.path)):
            app.invert_file(file)
