import pytest
from unittest.mock import patch, mock_open, ANY
from pathlib import Path
import os

# Ensure the project root is in the sys.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flort.cli import clean_content, generate_tree, list_files, is_binary_file,main

def test_clean_content():
    test_data = "line 1\n\nline 2\n\n\nline 3\n"
    expected_result = "line 1\nline 2\nline 3"
    with patch("builtins.open", mock_open(read_data=test_data)):
        assert clean_content("dummy_path") == expected_result

def test_is_binary_file(tmp_path):
    binary_file = tmp_path / "binary_file.bin"
    with open(binary_file, "wb") as f:
        f.write(b'\x00\x01\x02')

    text_file = tmp_path / "text_file.txt"
    text_file.write_text("This is a text file.")

    assert is_binary_file(binary_file) == True
    assert is_binary_file(text_file) == False

def test_generate_tree(tmp_path):
    d1 = tmp_path / "subdir1"
    d1.mkdir()
    (d1 / "file1.txt").write_text("content")
    (d1 / "file2.py").write_text("content")
    (d1 / "binary_file.bin").write_bytes(b'\x00\x01\x02')
    
    d2 = tmp_path / "subdir2"
    d2.mkdir()
    (d2 / "file3.txt").write_text("content")
    (d2 / ".hidden.txt").write_text("hidden content")
    
    expected_result = (
        f"|-- {d1.name}/\n"
        f"|   |-- file2.py\n"
        f"|   |-- file1.txt\n"
        f"|-- {d2.name}/\n"
        f"|   |-- file3.txt\n"
    )
    assert generate_tree([d1, d2], extensions=['.txt', '.py']) == expected_result

    # Test with --all flag
    expected_result_all = (
        f"|-- {d1.name}/\n"
        f"|   |-- file2.py\n"
        f"|   |-- file1.txt\n"
        f"|-- {d2.name}/\n"
        f"|   |-- file3.txt\n"
    )
    assert generate_tree([d1, d2], extensions=[], include_all=True, include_hidden=False) == expected_result_all

    # Adjust the order or inclusion of .hidden.txt in expected_result_hidden
    expected_result_hidden = (
        f"|-- {d1.name}/\n"
        f"|   |-- file2.py\n"
        f"|   |-- file1.txt\n"
        f"|-- {d2.name}/\n"
        f"|   |-- .hidden.txt\n"  # Ensure this is correctly positioned
        f"|   |-- file3.txt\n"
    )
    assert generate_tree([d1, d2], extensions=[], include_all=True, include_hidden=True) == expected_result_hidden

    # Test with no extensions and no --all flag
    expected_result_no_ext = ''
    assert generate_tree([d1, d2], extensions=[]) == expected_result_no_ext

def test_list_files(tmp_path):
    d1 = tmp_path / "subdir1"
    d1.mkdir()
    (d1 / "file1.txt").write_text("content")
    (d1 / "file2.py").write_text("content")
    (d1 / "binary_file.bin").write_bytes(b'\x00\x01\x02')
    
    d2 = tmp_path / "subdir2"
    d2.mkdir()
    (d2 / "file3.txt").write_text("content")
    (d2 / ".hidden.txt").write_text("hidden content")
    
    expected_result = (
        f"Path: {d1 / 'file2.py'}\nFile: file2.py\n-------\ncontent\n"
        f"Path: {d1 / 'file1.txt'}\nFile: file1.txt\n-------\ncontent\n"
        f"Path: {d2 / 'file3.txt'}\nFile: file3.txt\n-------\ncontent"
    )
    assert list_files([d1, d2], extensions=['.txt', '.py']) == expected_result

    # Test with --all flag
    expected_result_all = (
        f"Path: {d1 / 'file2.py'}\nFile: file2.py\n-------\ncontent\n"
        f"Path: {d1 / 'file1.txt'}\nFile: file1.txt\n-------\ncontent\n"
        f"Path: {d2 / 'file3.txt'}\nFile: file3.txt\n-------\ncontent"
    )
    assert list_files([d1, d2], include_all=True, include_hidden=False) == expected_result_all

    # Test with --hidden flag
    # Ensure the output includes .hidden.txt in the correct order
    expected_result_hidden = (
        f"Path: {d1 / 'file2.py'}\nFile: file2.py\n-------\ncontent\n"
        f"Path: {d1 / 'file1.txt'}\nFile: file1.txt\n-------\ncontent\n"
        f"Path: {d2 / '.hidden.txt'}\nFile: .hidden.txt\n-------\nhidden content\n"  # This line needs correct positioning
        f"Path: {d2 / 'file3.txt'}\nFile: file3.txt\n-------\ncontent"
    )
    assert list_files([d1, d2], include_all=True, include_hidden=True) == expected_result_hidden

    # Test with no extensions and no --all flag
    expected_result_no_ext = ''
    assert list_files([d1, d2], extensions=[]) == expected_result_no_ext

def test_list_files(tmp_path):
    d1 = tmp_path / "subdir1"
    d1.mkdir()
    (d1 / "file1.txt").write_text("content")
    (d1 / "file2.py").write_text("content")
    (d1 / "binary_file.bin").write_bytes(b'\x00\x01\x02')
    
    d2 = tmp_path / "subdir2"
    d2.mkdir()
    (d2 / "file3.txt").write_text("content")
    (d2 / ".hidden.txt").write_text("hidden content")
    
    # Test without ignore_dirs
    expected_result = (
        f"Path: {d1 / 'file2.py'}\nFile: file2.py\n-------\ncontent\n"
        f"Path: {d1 / 'file1.txt'}\nFile: file1.txt\n-------\ncontent\n"
        f"Path: {d2 / 'file3.txt'}\nFile: file3.txt\n-------\ncontent"
    )
    assert list_files([d1, d2], extensions=['.txt', '.py']) == expected_result

    # Test with --all flag
    expected_result_all = (
        f"Path: {d1 / 'file2.py'}\nFile: file2.py\n-------\ncontent\n"
        f"Path: {d1 / 'file1.txt'}\nFile: file1.txt\n-------\ncontent\n"
        f"Path: {d2 / 'file3.txt'}\nFile: file3.txt\n-------\ncontent"
    )
    assert list_files([d1, d2], include_all=True, include_hidden=False) == expected_result_all

    # Test with --hidden flag
    expected_result_hidden = (
        f"Path: {d1 / 'file2.py'}\nFile: file2.py\n-------\ncontent\n"
        f"Path: {d1 / 'file1.txt'}\nFile: file1.txt\n-------\ncontent\n"
        f"Path: {d2 / '.hidden.txt'}\nFile: .hidden.txt\n-------\nhidden content\n"
        f"Path: {d2 / 'file3.txt'}\nFile: file3.txt\n-------\ncontent"
    )
    assert list_files([d1, d2], include_all=True, include_hidden=True) == expected_result_hidden

    # Test with ignore_dirs parameter
    ignore_dirs = [str(d1)]  # Ignore the first directory
    expected_result_ignore_d1 = (
        f"Path: {d2 / 'file3.txt'}\nFile: file3.txt\n-------\ncontent"
    )
    assert list_files([d1, d2], extensions=['.txt', '.py'], ignore_dirs=ignore_dirs) == expected_result_ignore_d1

    # Test with ignore_dirs parameter (ignoring a non-existent directory)
    ignore_dirs_non_existent = [str(tmp_path / "nonexistent")]
    expected_result_ignore_non_existent = (
        f"Path: {d1 / 'file2.py'}\nFile: file2.py\n-------\ncontent\n"
        f"Path: {d1 / 'file1.txt'}\nFile: file1.txt\n-------\ncontent\n"
        f"Path: {d2 / 'file3.txt'}\nFile: file3.txt\n-------\ncontent"
    )
    assert list_files([d1, d2], extensions=['.txt', '.py'], ignore_dirs=ignore_dirs_non_existent) == expected_result_ignore_non_existent

    # Test with no extensions and no --all flag
    expected_result_no_ext = ''
    assert list_files([d1, d2], extensions=[]) == expected_result_no_ext
