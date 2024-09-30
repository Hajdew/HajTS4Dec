import uncompyle6
import os
import shutil
import zipfile
import logging
import struct
import traceback
import decompyle3
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from tkinter import Tk, Label, Button, filedialog, messagebox, Frame, Text, StringVar
from tkinter.font import Font
from datetime import datetime
from io import StringIO
from tqdm import tqdm


# Set up logging for errors
logging.basicConfig(filename='decompilation_errors.log', level=logging.ERROR)


def get_pyc_info(file_path):
    """Extracts the magic number and timestamp from the .pyc file."""
    with open(file_path, 'rb') as f:
        magic = f.read(4)
        # Get the current date and time with milliseconds
        current_datetime = datetime.now()
        timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return magic, timestamp

def decompile_pyc(file_info, temp_dir, output_dir):
    root, file = file_info
    bytecode_file = os.path.join(root, file)

    # Create the corresponding directory in the output folder
    relative_path = os.path.relpath(root, temp_dir)
    target_dir = os.path.join(output_dir, relative_path)
    os.makedirs(target_dir, exist_ok=True)

    # Output file path for the decompiled Python file (removes .pyc extension)
    decompiled_file_path = os.path.join(target_dir, f'{file[:-4]}.py')

    try:
        with open(decompiled_file_path, 'w') as f:
            string_io = StringIO()
            uncompyle6.decompile_file(bytecode_file, string_io)
            f.write(string_io.getvalue())
        return f"{decompiled_file_path} decompiled successfully."
    except uncompyle6.semantics.pysource.SourceWalkerError as e:
        error_message = f"Failed to decompile with uncompyle6 {bytecode_file}: {str(e)}"
        logging.error(error_message)  # Log the error to the file
        print(error_message)

        # Get and log .pyc file info
        magic, timestamp = get_pyc_info(bytecode_file)
        logging.error(f"Magic: {magic}, Timestamp: {timestamp}")

        # Attempt decompilation with decompyle3
        try:
            with open(decompiled_file_path, 'w') as f:
                decompyle3.decompile_file(bytecode_file, f)
                logging.error(f"{decompiled_file_path} decompiled successfully with decompyle3.")
                # Get and log .pyc file info
                magic, timestamp = get_pyc_info(bytecode_file)
                logging.error(f"Magic: {magic}, Timestamp: {timestamp}")
            return f"{decompiled_file_path} decompiled successfully with decompyle3."

        except Exception as e:
            decompile_error_message = f"Also failed with decompyle3: {str(e)}"
            logging.error(decompile_error_message)
            logging.error(traceback.format_exc())
            print(decompile_error_message)
            return decompile_error_message

def copy_files(file_info, temp_dir, output_dir):
    root, file = file_info
    bytecode_file = os.path.join(root, file)

    # Create the corresponding directory in the output folder
    relative_path = os.path.relpath(root, temp_dir)
    target_dir = os.path.join(output_dir, relative_path)
    os.makedirs(target_dir, exist_ok=True)

    # Output file path in the target directory (keeps .pyc extension)
    target_file_path = os.path.join(target_dir, file)

    try:
        # Copy the file from temp_dir to output_dir
        shutil.copy(bytecode_file, target_file_path)
        return f"{target_file_path} copied successfully."
    except Exception as e:
        error_message = f"Failed to copy {bytecode_file}: {str(e)}"
        logging.error(error_message)  # Log the error to the file
        print(error_message)
        return error_message

# Function to run the decompilation process
def start_decompiling():
    print("start")
    input_path = input_file.get()
    print(input_file.get())
    if not input_path or not input_path.endswith('.ts4script'):
        messagebox.showerror("Error", "Please select a valid .ts4script file")
        return

    output_dir = './modfile_decompiled/'
    temp_dir = './temp_extract/'

    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)


    console_text.insert('1.0', 'Unzip ts3script \n')
    root.update()


    # Step 1: Unzip the .ts4script file into a temporary directory
    with zipfile.ZipFile(input_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    print("extracted")
    console_text.insert('1.0', 'Gather files \n')
    root.update()

    # Step 2: Get a list of all files to process
    all_pyc_files = []
    another_files = []
    for roots, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith('.pyc'):
                all_pyc_files.append((roots, file))
            else:
                another_files.append((roots, file))
    
    console_text.insert('1.0', 'Decompyle files \n')
    root.update()

    print("init multicore")

    # Step 3: Use ProcessPoolExecutor to decompile in parallel
    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(decompile_pyc, file_info, temp_dir, output_dir): file_info
            for file_info in all_pyc_files
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc="Decompiling files", unit="file"):
            result = future.result()
            # print(result)
            console_text.insert('1.0',future.result()+ " \n")
            root.update()
    
    console_text.insert('1.0', 'Copy not .pyc files \n')
    root.update()

    # Step 3.5: Use ProcessPoolExecutor to copy in parallel
    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(copy_files, file_info, temp_dir, output_dir): file_info
            for file_info in another_files
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc="Copy files", unit="file"):
            result = future.result()
            # print(result)
            console_text.insert('1.0',future.result()+ " \n")
            root.update()
    
    # Step 4: Clean up the temporary directory  
    console_text.insert('1.0',"cleaning \n")
    root.update()
    print("cleaning")
    shutil.rmtree(temp_dir)
    print("cleaned")
    console_text.insert('1.0',"cleaned \n")
    root.update()

    
    progress_label.config(text=f"Decompiled files saved to {output_dir}")
    messagebox.showinfo("Complete", f"Decompiled files saved to {output_dir}")


# Function to select the input .ts4script file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("TS4 Script", "*.ts4script")])
    if file_path:
        input_file.set(file_path)
        print(file_path)
        Selected_file.config(text=f"Selected: {file_path}").pack()


if __name__ == '__main__':
    multiprocessing.freeze_support()  # For Windows, prevents the script from being re-executed in subprocesses


    # Create the tkinter GUI
    root = Tk()
    root.resizable(width=False, height=False)
    root.title("TS4Script Decompiler")

    text_font = Font(family="Helvetica", size=15)


    # Variable to store the selected file path
    input_file = StringVar()

    # Create and place the label and buttons
    Label(root, text="Select .ts4script file:",font=text_font).pack(pady=10)

    select_button = Button(root, text="Browse", command=select_file,font=text_font,padx=10)
    select_button.pack()

    Selected_file = Label(root, text="Selected:",font=text_font,padx=10)
    Selected_file.pack()

    decompile_button = Button(root, text="Start Decompiling", command=start_decompiling,font=text_font)
    decompile_button.pack(pady=20)

    progress_label = Label(root, text="",font=text_font)
    progress_label.pack()

        # Add a button to toggle console output
    Label(root, text="Output:").pack(side="top", anchor="nw")

    # Console output frame (hidden by default)
    console_frame = Frame(root)
    console_frame.pack()

    console_text = Text(console_frame, height=10,borderwidth=2, wrap="word",font=text_font)
    console_text.pack(side="left", fill="both", expand=True,padx=10, pady=10)

    # Start the GUI event loop
    root.mainloop()
