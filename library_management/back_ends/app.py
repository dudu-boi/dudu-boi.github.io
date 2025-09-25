import sys
import os
from models import DownloadReport
from routes import get_input_file
from downloader import YtDlpHyperdrive, banner 

if __name__ == "__main__":
    banner()
    path = get_input_file()

    if not os.path.isfile(path):
        print(f"File not found: {path}")
        sys.exit(1)

    app = YtDlpHyperdrive()
    app.run(path)