# dir2json

Simple Python script to quickly iterate through all the files in a specified directory and all subdirectories.

## Features

- Recursively scans directories and outputs file information to JSON
- Filter files by name pattern
- Include or exclude directories
- Add MIME type information based on file extension
- Filter files by age (include only files modified within a specified number of days)

## Usage

```
python dir2json.py --folder /path/to/scan --outfile output.json [options]
```

### Options

- `--folder`, `-f`: Directory to scan (required)
- `--outfile`, `-o`: JSON file to write results to (required)
- `--match`, `-m`: Filename pattern to match (default: *)
- `--mime`: Include MIME type information based on file extension
- `--no-mime`: Don't include MIME type information (default)
- `--dirs`: Include directories in results
- `--no-dirs`: Don't include directories (default)
- `--max-age`: Maximum age of files in days (only include files modified within this period)

## Example

```
python dir2json.py --folder ~/Documents --outfile docs.json --mime --max-age 30
```

This will scan all files in the Documents folder, include MIME type information, and only include files modified in the last 30 days.

