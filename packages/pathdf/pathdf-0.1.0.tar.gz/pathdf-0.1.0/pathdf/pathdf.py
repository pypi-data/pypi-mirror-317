from pathlib import Path
import pandas as pd

def pathdf(data_dir, output_dir, output_file, suffixes, file_format):
    # Create empty image_list
    image_list = []
    # Make path variable for data directory parent directory
    project_data_dir = Path(data_dir)

    # Iterate through each parent directory to search for each sub directory
    for subdir in project_data_dir.iterdir():
        # check if subdir is directory
        if subdir.is_dir():
            # iterate over files in subdir and check files are images and end with specified suffixes
            for image_path in subdir.iterdir():
                if image_path.suffix in suffixes:
                    # add image_path and subdir name to image_list
                    image_list.append([image_path, subdir.name])

    # Create empty dataframe with columns image_path and label
    df = pd.DataFrame(image_list, columns=["image_path", "infection_status"])
    # check if df is non-empty , if non-empty print dataframe creates successfully else print error message " Dataframe is empty , check error"
    if not df.empty:
        print("Dataframe created successfully")
    else:
        print("Dataframe is empty, check error")

    # Create the output directory if it doesn't exist
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Define the full path to the output file
    output_path = output_dir_path / output_file

    # Write dataframe to the specified format
    if file_format == 'csv':
        df.to_csv(output_path, index=False)
    elif file_format == 'txt':
        df.to_csv(output_path, index=False, sep='\t')
    elif file_format == 'xlsx':
        df.to_csv(output_path, index=False , sep='\t')
    else:
        print(f"Unsupported file format: {file_format}")
        return

    print(f'File {output_path} created successfully.')