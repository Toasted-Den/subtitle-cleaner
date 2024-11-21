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
            if "-->" in line:  # Write timestamp lines as-is
                f_output.write(line + '\n')
            elif line.isdigit() or not line:  # Write sequence numbers and empty lines as-is
                f_output.write(line + '\n')
            else:
                # Process text lines by removing punctuation and converting to lowercase
                line = line.replace(',', '').replace('.', '').replace('!', '').lower()
                f_output.write(line + '\n')

def process_all_srt_files():
    """
    Process all .srt files in the current directory.

    Returns:
        None
    """
    srt_files = [file for file in os.listdir('.') if file.lower().endswith('.srt')]
    if not srt_files:
        print("No .srt files found in the directory.")
        return

    for file in srt_files:
        process_srt_file(file)
        print(f"Processed: {file}")

if __name__ == "__main__":
    process_all_srt_files()