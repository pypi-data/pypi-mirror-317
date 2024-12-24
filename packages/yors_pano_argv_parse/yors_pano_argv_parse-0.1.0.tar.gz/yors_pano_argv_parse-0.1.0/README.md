<!-- inject desc here -->
<!-- inject-desc -->

parse argv-like args in python

## Features

<!-- inject feat here -->

- feat(core): parse stro or stra to nano

## Usage

```bash
pip install yors_pano_argv_parse
```

## Demo

<!-- inject demo here -->

```py
# # from main import nanoargs
from yors_pano_argv_parse import nanoargs
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_data = sys.argv[1:] if len(sys.argv) > 2 else sys.argv[1]
        parsed = nanoargs(input_data)
        print(f"Parsed argv: {parsed.argv}")
        print(f"Parsed flags: {parsed.flags}")
        print(f"Parsed extras: {parsed.extras}")
    else:
        print("Please provide command line arguments to parse.")
```
