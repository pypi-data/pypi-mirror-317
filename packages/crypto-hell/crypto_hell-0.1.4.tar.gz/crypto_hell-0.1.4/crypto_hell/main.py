import os

def create_combined_python_script():
    # Get all .m files in the current directory
    m_files = [file for file in os.listdir('.') if file.endswith('.m')]
    
    # Name of the combined Python file
    combined_file_name = "combined_m_files.py"
    
    with open(combined_file_name, 'w') as combined_file:
        for m_file in m_files:
            # Read the content of each .m file
            with open(m_file, 'r') as f:
                content = f.read()
            
            # Write the content into the combined Python file
            combined_file.write(content)
            combined_file.write("\n" + "-" * 14 + "\n\n")
    
    print(f"Generated {combined_file_name}")

if __name__ == "__main__":
    create_combined_python_script()
