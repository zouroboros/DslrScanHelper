import sys

from dslr_scan_helper.debug_context import DebugContext
from dslr_scan_helper.app import DslrScanHelperApp, DslrScanHelperContext

if __name__ == "__main__":
    context = DslrScanHelperContext()
    #context = DebugContext()
    app = DslrScanHelperApp(context)
    converted_files = app.convert(sys.argv[1:])
    for file in converted_files:
        cropped = app.crop_file(file)
        app.invert(cropped)

    context.end()
