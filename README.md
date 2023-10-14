# SRT Subtitle Cleaner

The SRT Subtitle Cleaner is a Python script that processes SubRip Subtitle (SRT) files. It removes all capital letters, converts them to lowercase, and removes all periods, commas, and exclamation marks from the subtitle text. The processed output is saved in a new SRT file with the same content but in lowercase and without these punctuation marks.

This script was specifically made to fit my subtitle editing style, as seen in my [videos](https://youtube.com/@ToastedDen).

## Getting Started

1. **Download the Script**: Download the `sub.py` script from the repository.

2. **Place the Script**: Move the `sub.py` script to the directory containing your SRT files. For example, create a folder named "subtitles" and place the script there alongside your SRT files.

## Usage

You can run the script using the following command:

- `[input.srt]`: Replace this with the name of the specific SRT file you want to process. The processed output will be saved as `[input]_processed.srt` in the same directory.

- `-all`: Use this argument to process all SRT files in the current directory and its subdirectories. The processed files will be saved in the same locations with the suffix `_processed.srt`.

**Optional - Add to PATH**

If you want to run the script from any directory without specifying the full path, you can add the directory containing `sub.py` to your system's PATH.

**Windows:**

1. Press `Win + R` to open the Run dialog.
2. Type `sysdm.cpl` and press Enter. This opens the System Properties window.
3. In the System Properties window, go to the "Advanced" tab.
4. Click the "Environment Variables" button at the bottom.
5. In the "System variables" section, find the `PATH` variable and click "Edit."
6. Click "New" and add the path to the directory containing `sub.py`. For example, if you placed the script in `C:\subtitle cleaner`, add `C:\subtitle cleaner` to the PATH.
7. Click "OK" to save the changes.

Now, you can run the script from any directory by simply using the `sub.py` command.

## Examples

1. Process a specific SRT file:

The processed output will be saved as `input_processed.srt` in the same directory.

2. Process all SRT files in the current directory and its subdirectories:

Processed files will be saved in their respective locations with the suffix `_processed.srt`.

## If you have any questions...

Feel free to add me on Discord, and I can try to help you out.
Discord: toastedden OR Toasted Den#0001

## Also check out my [website](https://toastedden.com/)!

*Paint me yellow and call me sunshine; you've made it to the bottom!*
