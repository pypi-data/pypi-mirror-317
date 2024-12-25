## TurboDL

![PyPI - Version](https://img.shields.io/pypi/v/turbodl?style=flat&logo=pypi&logoColor=blue&color=blue&link=https://pypi.org/project/turbodl)
![PyPI - Downloads](https://img.shields.io/pypi/dm/turbodl?style=flat&logo=pypi&logoColor=blue&color=blue&link=https://pypi.org/project/turbodl)
![PyPI - Code Style](https://img.shields.io/badge/code%20style-ruff-blue?style=flat&logo=ruff&logoColor=blue&color=blue&link=https://github.com/astral-sh/ruff)
![PyPI - Format](https://img.shields.io/pypi/format/turbodl?style=flat&logo=pypi&logoColor=blue&color=blue&link=https://pypi.org/project/turbodl)
![PyPI - Python Compatible Versions](https://img.shields.io/pypi/pyversions/turbodl?style=flat&logo=python&logoColor=blue&color=blue&link=https://pypi.org/project/turbodl)

TurboDL is an extremely smart and efficient download manager for various cases.

- Support for the modern HTTP/2 protocol for faster downloads.
- Built-in download acceleration.
- Uses your connection speed to download even more efficiently.
- Retries failed requests.
- Automatically detects the file type, name, extension, and size.
- Automatically handles redirects.
- Automatically validates the hash of the downloaded file.
- Shows a fancy and precise progress bar.

<br>

#### Installation (from [PyPI](https://pypi.org/project/turbodl))

```bash
pip install -U turbodl  # Install the latest version of TurboDL
```

### Example Usage

#### Inside a Python script

```python
from turbodl import TurboDL


turbodl = TurboDL(
    max_connections='auto',
    connection_speed=80,
    show_optimization_progress_bar=True,
    show_progress_bar=True,
    custom_headers=None,
    timeout=None
)

turbodl.download(
    url='https://example.com/file.txt',
    output_path='path/to/file',
    expected_hash='********',  # Or None if you don't want to check the hash
    hash_type='sha256'
)
# >>> file.txt ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 35.6/35.6 kB 36.2 MB/s 0:00:00 100%

# All functions are documented and have detailed typings, use your development IDE to learn more.

```

#### From the command line

```bash
turbodl --help
# >>> ╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# >>> │ *    url              TEXT           The download URL to download the file from. [default: None] [required]                                                                                                                  │
# >>> │      output_path      [OUTPUT_PATH]  The path to save the downloaded file to. If the path is a directory, the file name will be generated from the server response. If the path is a file, the file will be saved with the   │
# >>> │                                      provided name. If not provided, the file will be saved to the current working directory. (default: Path.cwd())                                                                          │
# >>> │                                      [default: None]                                                                                                                                                                         │
# >>> ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
# >>> ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# >>> │ --max-connections                 -mc                                           INTEGER  The maximum number of connections to use for downloading the file (default: 'auto'). [default: None]                                │
# >>> │ --connection-speed                -cs                                           FLOAT    Your connection speed in Mbps (default: 80). [default: None]                                                                        │
# >>> │ --overwrite                       -o    --no-overwrite                    -no            Overwrite the file if it already exists. Otherwise, a "_1", "_2", etc. suffix will be added. [default: overwrite]                   │
# >>> │ --show-optimization-progress-bar  -sop  --hide-optimization-progress-bar  -hop           Show or hide the initial optimization progress bar. [default: show-optimization-progress-bar]                                       │
# >>> │ --show-progress                   -sp   --hide-progress                   -hp            Show or hide the download progress bar. [default: show-progress]                                                                    │
# >>> │ --timeout                         -t                                            INTEGER  Timeout in seconds for the download process. Or None for no timeout. [default: None]                                                │
# >>> │ --install-completion                                                                     Install completion for the current shell.                                                                                           │
# >>> │ --show-completion                                                                        Show completion for the current shell, to copy it or customize the installation.                                                    │
# >>> │ --help                                                                                   Show this message and exit.                                                                                                         │
# >>> ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

turbodl https://example.com/file.txt [...] path/to/file  # Tip: use -cs argument to set your connection speed and accelerate the download
# >>> file.txt ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 35.6/35.6 kB 36.2 MB/s 0:00:00 100%
```

### Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, fork the repository and create a pull request. You can also simply open an issue and describe your ideas or report bugs. **Don't forget to give the project a star if you like it!**

1. Fork the project;
2. Create your feature branch ・ `git checkout -b feature/{feature_name}`;
3. Commit your changes ・ `git commit -m "{commit_message}"`;
4. Push to the branch ・ `git push origin feature/{feature_name}`;
5. Open a pull request, describing the changes you made and wait for a review.

### Disclaimer

Please note that downloading copyrighted content from some services may be illegal in your country. This tool is designed for educational purposes only. Use at your own risk.
