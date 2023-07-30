import sys
import os

def process_srt_file(input_file):
    output_file = input_file.replace('.srt', '_processed.srt')
    with open(input_file, 'r') as f_input, open(output_file, 'w') as f_output:
        for line in f_input:
            line = line.replace('.', '').lower()
            f_output.write(line)

def process_all_srt_files():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.lower().endswith('.srt'):
                input_file = os.path.join(root, file)
                process_srt_file(input_file)
                print(f"Processed: {input_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sub.py input.srt | all")
    else:
        input_file = sys.argv[1]
        if input_file.lower() == "all":
            process_all_srt_files()
        elif not input_file.lower().endswith('.srt'):
            print("Please provide an .srt file or use 'all' to process all files.")
        else:
            process_srt_file(input_file)
            print("Processing complete.")
