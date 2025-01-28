import os
import pyperclip  # Library for clipboard manipulation
import re # Library for regular expressions

def convert_to_snippet(file_path) -> bool:
    """
    Converts the contents of a given file to a VSCode snippet format and copies it to the clipboard.

    Args:
        file_path (str): The path to the file to convert.
    
    Returns:
        bool: True if the conversion was successful, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found. Please try again.")
        return False

    try:
        # Read file content
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Convert to snippet body format
        snippet_body = []
        for line in lines:
            # Escape special characters (especially " and newlines)
            # Replace double quotes with escaped double quotes
            # line = line.replace('"', '\\"')
            line = re.sub('"', '\\"', line)

            # Replace newline characters with escaped newline characters
            
            line = line.replace('\\n', '\\\\n')
            # line = re.sub('\\n','\\\\n', line)

            # Remove trailing newline characters
            line = re.sub('\\n$', '', line)
            
            # Append line to snippet body
            snippet_body.append(f'"{line}"')

        # Join lines into snippet format
        snippet_output = '[\n' + ',\n'.join(snippet_body) + '\n]'

        # Copy output to clipboard
        pyperclip.copy(snippet_output)
        print("\n✅ Snippet converted and copied to clipboard successfully!")
        print("\nPreview of the snippet:")
        print(snippet_output)
        print("\nYou can now paste the snippet in your VSCode user snippets file.")
        print("スニペットの変換に成功しました！")
        print("変換された\"[body]\"はクリップボードにコピーされました。")
        print("スニペットを VSCode のユーザースニペットファイルに貼り付けることができます。")
        return True
    except Exception as e:
        print(f"Error while processing the file: {e}")
        return False

if __name__ == "__main__":
    print("Welcome to the Snippet Converter!")
    print("スニペットのbodyを作成します。")
    print("Please enter the file name to convert:")
    
    while True:
        file_name = input("> File name: ").strip()
        if file_name:
            success = convert_to_snippet(file_name)
            if success:
                break
        else:
            print("❌ No file name provided. Please try again.")
