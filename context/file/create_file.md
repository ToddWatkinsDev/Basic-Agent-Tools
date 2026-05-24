# create_file

## Purpose
Creates a new file at the specified path. Will not overwrite an existing file. Automatically creates any missing parent directories.

Use this tool when you need to create a blank file or a file with initial content. If you need to overwrite an existing file or append to one, use `write_to_file` instead.

## Inputs
| Argument | Type | Required | Description |
|---|---|---|---|
| `filepath` | string | Yes | Path to the file to create (e.g. `output/report.txt`) |
| `content` | string | No | Initial content to write into the file (default: empty) |

## Outputs
- `"Empty file created: <filepath>"` — file was created with no content
- `"File created with content: <filepath>"` — file was created with initial content
- `"File already exists: <filepath>"` — file was not modified
- `"Error creating file: <reason>"` — something went wrong

## Usage
```bash
# Create an empty file
python tools/file/create_file.py output/notes.txt

# Create a file with initial content
python tools/file/create_file.py output/notes.txt "Hello World"
```

## Notes
- Parent directories are created automatically if they do not exist
- Existing files are never overwritten — use `write_to_file` for that
- Encoding is always UTF-8
