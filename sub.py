import sys
import os

def process_srt_file(input_file):
    """
    Process the subtitle file specified by 'input_file' and write the processed content to a new file.

    Parameters:
        input_file (str): The path to the input subtitle file (.srt).

    Returns:
        None
    """
    output_file = input_file.replace('.srt', '_processed.srt')  # Create a new filename for the processed output
    with open(input_file, 'r') as f_input, open(output_file, 'w') as f_output:
        for line in f_input:
            line = line.strip()
            if "-->" in line:  # Check if the line contains a timestamp (an arrow)
                f_output.write(line + '\n')  # Write the timestamp line as-is with a newline
            else:
                if line.isdigit() or not line:  # Check if the line is empty or a sequence number
                    f_output.write(line + '\n')  # Write empty lines or sequence numbers as-is
                else:
                    line = line.replace('.', '').replace(',', '').lower()  # Process the subtitle text line
                    f_output.write(line + '\n')  # Write the processed subtitle text with a newline

def process_all_srt_files():
    """
    Process all .srt files in the current directory and its subdirectories.

    Parameters:
        None

    Returns:
        None
    """
    for root, dirs, files in os.walk('.'):  # Traverse the directory tree
        for file in files:
            if file.lower().endswith('.srt'):  # Check if the file has a .srt extension
                input_file = os.path.join(root, file)  # Get the full path of the .srt file
                process_srt_file(input_file)  # Process the .srt file
                print(f"Processed: {input_file}")  # Print a message indicating the file has been processed

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sub.py input.srt | all")  # Print usage instructions if the script is not used correctly
    else:
        input_file = sys.argv[1]
        if input_file.lower() == "all":
            process_all_srt_files()  # Process all .srt files in the current directory and its subdirectories
        elif not input_file.lower().endswith('.srt'):
            print("Please provide an .srt file or use 'all' to process all files.")  # Print a message for invalid input
        else:
            process_srt_file(input_file)  # Process the specified .srt file
            print("Processing complete.")  # Print a message to indicate processing is finished
