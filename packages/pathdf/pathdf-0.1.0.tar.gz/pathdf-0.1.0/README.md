# pathdf

A package to convert file paths to CSV or any format .

## Installation

```sh
pip install pathdf

Usage : 

from pathdf import pathdf

data_dir = "path/to/data"
output_dir = "path/to/output"
output_file = "files_df"
suffixes = [".png", ".jpg", ".txt", ".MRI"]
file_format = "csv"  # Options: "csv", "txt", "excel"
pathdf(data_dir, output_dir, f"{output_file}.{file_format}", suffixes, file_format)