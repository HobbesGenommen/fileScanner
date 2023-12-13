import os
import time
import sys

target_extensions = ['.py', '.bat', '.rar', '.cab', '.tar.gz', '.exe', '.js', '.jar', '.vbs', '.ps1', '.scr', '.com', '.sh', '.dll']
search_words = ['trojan ', 'WannaCry', 'Conficker', 'Zeus', 'Locky', 'dataminer', 'cryptominer', 'coinhive', ' hack ', ' crack ', ' hijack ', ' spoof ', 'evasion ', ' cloak ', ' steal', 'buffer overflow', 'remote execution', 'privilege escalation', 'bypass security', 'silent installation', 'system compromise', 'run as administrator', 'install silent']


def count_files_in_directory(directory, target_extensions):
    print("counting the files to scan... ")
    total_files = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(target_extensions)):
                total_files += 1
    
    return total_files

def scan_directory(directory, target_extensions, search_words_finally, total_files):
    found_files = []
    scanned_files = 0

    start_time = time.time()

    def update_scanned_files():
        nonlocal scanned_files
        scanned_files += 1
        sys.stdout.write(f'\rScanned Files: {scanned_files} of {total_files} files')
        sys.stdout.flush()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(target_extensions)):
                file_path = os.path.join(root, file)
                matching_word = search_words_in_file(file_path, search_words_finally)
                if matching_word:
                    found_files.append((file_path, matching_word))
                update_scanned_files()
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    return found_files, elapsed_time

def search_words_in_file(file_path, search_words_finally):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
            for word in search_words_finally:
                if word.lower() in file_contents.lower():
                    return word
    except Exception as e:
        pass
    
    return None

if __name__ == "__main__":
    target_directory = input("Enter the directory path to scan, C:\Windows\System32\ would be an example: ")
    search_words_confirmation = input("Do you want to use the recommended words to search for? (y/n): ")
    
    if search_words_confirmation == 'y':
        search_words_finally = search_words
        
        if os.path.isdir(target_directory):
            total_files = count_files_in_directory(target_directory, target_extensions)
            confirmation = input(f"{total_files} files found. Do you want to start scanning? (y/n): ").strip().lower()
            
            if confirmation == 'y':
                found_files, elapsed_time = scan_directory(target_directory, target_extensions, search_words_finally, total_files)
            
                if found_files:
                    print("\nFiles containing the specified words:")
                    for file, word in found_files:
                        print(f"{word} : {file}")
                else:
                    print("\nNo files containing the specified words found.")
            else:
                print("Scan canceled.")
        else:
            print("Invalid directory path.")
    else:
        search_words_finally = input("Write the word, you want to search for and press enter (it may not work correctly): ")
        
        if os.path.isdir(target_directory):
            total_files = count_files_in_directory(target_directory, target_extensions)
            confirmation = input(f"{total_files} files found. Do you want to start scanning? (y/n): ").strip().lower()
            
            if confirmation == 'y':
                found_files, elapsed_time = scan_directory(target_directory, target_extensions, search_words_finally, total_files)
            
                if found_files:
                    print("\nFiles containing the specified words:")
                    for file, word in found_files:
                        print(f"{word} : {file}")
                else:
                    print("\nNo files containing the specified words found.")
            else:
                print("Scan canceled.")
        else:
            print("Invalid directory path.")

end = input("Press enter to close")
