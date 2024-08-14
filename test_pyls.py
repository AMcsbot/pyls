import pytest
import os
from datetime import datetime
from pyls import getDescriptionsOfFilesInDir, formatResults

# Test getDescriptionsOfFilesInDir function
def test_getDescriptionsOfFilesInDir(tmpdir):
    # Setup: Create some files and directories in a temporary directory
    dirpath = tmpdir.mkdir("testdir")
    file1 = dirpath.join("file1.txt")
    file1.write("content")
    subdir = dirpath.mkdir("subdir")
    executable = dirpath.join("executable.sh")
    executable.write("run")
    executable.chmod(0o755)

    # Act: Call the function
    results = getDescriptionsOfFilesInDir(str(dirpath))

    # Assert: Verify the results
    filenames = [f['filename'] for f in results]
    assert "file1.txt" in filenames
    assert "subdir" in filenames
    assert "executable.sh" in filenames

    filetypes = {f['filename']: f['filetype'] for f in results}
    assert filetypes["file1.txt"] == "f"
    assert filetypes["subdir"] == "d"
    assert filetypes["executable.sh"] == "x"

# Test formatResults function
def test_formatResults():
    # Setup: Create mock file descriptions
    results = [
        {
            "filename": "file1.txt",
            "filetype": "f",
            "modtime": datetime(2024, 8, 14, 10, 30, 0),
            "filesize": 100,
        },
        {
            "filename": "subdir",
            "filetype": "d",
            "modtime": datetime(2024, 8, 14, 11, 0, 0),
            "filesize": 0,
        },
        {
            "filename": "executable.sh",
            "filetype": "x",
            "modtime": datetime(2024, 8, 14, 11, 30, 0),
            "filesize": 50,
        },
    ]

    # Act & Assert: Test different formats
    formatted_lines = formatResults(results, long_format=False, filetype=False)
    assert formatted_lines == ["file1.txt", "subdir", "executable.sh"]

    formatted_lines = formatResults(results, long_format=True, filetype=False)
    assert formatted_lines == [
        "2024-08-14 10:30:00         100  file1.txt",
        "2024-08-14 11:00:00           0  subdir",
        "2024-08-14 11:30:00          50  executable.sh",
    ]

    formatted_lines = formatResults(results, long_format=False, filetype=True)
    assert formatted_lines == ["file1.txt", "subdir/", "executable.sh*"]

    formatted_lines = formatResults(results, long_format=True, filetype=True)
    assert formatted_lines == [
        "2024-08-14 10:30:00         100  file1.txt",
        "2024-08-14 11:00:00           0  subdir/",
        "2024-08-14 11:30:00          50  executable.sh*",
    ]
