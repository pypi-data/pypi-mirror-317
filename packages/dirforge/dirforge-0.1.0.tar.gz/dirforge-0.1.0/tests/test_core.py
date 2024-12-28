
from pathlib import Path
from dirforge import create_directory_tree, get_depth, clean_name

def test_get_depth():
    assert get_depth('├── file.txt') == 0
    assert get_depth('│   ├── nested.txt') == 1
    assert get_depth('│   │   └── deep.txt') == 2

def test_clean_name():
    assert clean_name('├── file.txt') == 'file.txt'
    assert clean_name('└── folder/') == 'folder'
    assert clean_name('│   ├── nested.txt') == 'nested.txt'

def test_create_directory_tree(tmp_path):
    # Create a temporary test file
    test_tree = """
    root/
    ├── folder1/
    │   ├── file1.txt
    │   └── file2.txt
    └── folder2/
        └── file3.txt
    """
    test_file = tmp_path / "test_tree.txt"
    test_file.write_text(test_tree)
    
    # Run the function
    create_directory_tree(str(test_file))
    
    # Check if directories and files were created
    assert (tmp_path / "root").is_dir()
    assert (tmp_path / "root" / "folder1").is_dir()
    assert (tmp_path / "root" / "folder1" / "file1.txt").is_file()
    assert (tmp_path / "root" / "folder1" / "file2.txt").is_file()
    assert (tmp_path / "root" / "folder2").is_dir()
    assert (tmp_path / "root" / "folder2" / "file3.txt").is_file()