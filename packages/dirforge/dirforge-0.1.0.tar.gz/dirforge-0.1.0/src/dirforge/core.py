import os
from pathlib import Path

def get_depth(line):
    """Calculate the depth of a line based on its indentation and tree symbols."""
    count = 0
    for char in line:
        if char in ['│', '├', '└', ' ']:
            count += 1
        else:
            break
    return count // 4  # Standard tree indentation is 4 spaces

def clean_name(line):
    """Remove tree symbols and whitespace from the line."""
    # Remove tree symbols and trim whitespace
    name = line.replace('├── ', '').replace('└── ', '').replace('│   ', '').replace('│', '').strip()
    return name

def create_directory_tree(input_file):
    """Create directory structure from a text file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.rstrip() for line in f if line.strip()]

        # Initialize structure tracking
        current_path = Path.cwd()
        path_stack = []
        last_depth = -1

        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

            # Get depth and clean name
            depth = get_depth(line)
            name = clean_name(line)

            # Skip if name is empty or contains only tree symbols
            if not name or name in ['├', '└']:
                continue

            # Remove trailing slash if present
            name = name.rstrip('/')

            # Adjust path stack based on depth
            if depth <= last_depth:
                # Pop items from stack when going back up or staying at same level
                for _ in range(last_depth - depth + 1):
                    if path_stack:
                        path_stack.pop()

            # Add current item to stack
            path_stack.append(name)
            last_depth = depth

            # Create the full path
            full_path = current_path
            for path_part in path_stack:
                full_path = full_path / path_part

            if not full_path.suffix:  # No extension means it's a directory
                full_path.mkdir(exist_ok=True)
                print(f"Created directory: {full_path}")
            else:
                # Ensure parent directories exist
                full_path.parent.mkdir(parents=True, exist_ok=True)
                # Create empty file
                full_path.touch(exist_ok=True)
                print(f"Created file: {full_path}")

        print("\nDirectory tree creation completed successfully!")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    create_directory_tree(input_file)