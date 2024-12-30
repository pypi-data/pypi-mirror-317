# __init__.py
__description__ = 'NoteBin, A tool package for writing notes for Mr. CaoBin'
__author__ = 'Bin Cao, Advanced Materials Thrust, Hong Kong University of Science and Technology (Guangzhou)'
__author_email__ = 'binjacobcao@gmail.com'

import datetime
from .notetaker import process_all_md_files

# Get the current date and time in the desired format
now = datetime.datetime.now()
formatted_date_time = now.strftime('%Y-%m-%d %H:%M:%S')

# Print introductory information
print('NoteBin, A tool package for writing notes')
print('If you need any help, please contact me at github.com/Bin-Cao')
print('Executed on:', formatted_date_time, ' | Have a great day.')
print('=' * 80)

# Replace this with the path to the directory you want to process
directory_to_process = "./"  # You can change this path if needed
print(f"Processing files in directory: {directory_to_process}")
process_all_md_files(directory_to_process)
