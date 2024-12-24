import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fs2f.fs2f import fs2f, f2fs, hash


@pytest.fixture
def setup_test_dirs(tmpdir):
    # Create a test structure
    input_dir = tmpdir.mkdir("input")
    output_dir = tmpdir.mkdir("output")
    shapshot = tmpdir.join("structure.fs")

    # Add files to the input directory
    input_dir.join("test_file.txt").write("This is a test file.")
    input_dir.mkdir("subdir").join("nested_file.txt").write("Nested file content.")

    return str(input_dir), str(output_dir), str(shapshot)


def test(setup_test_dirs):
    input_dir, output_dir, shapshot = setup_test_dirs

    # Test the creation of a snapshot
    fs2f(input_dir, shapshot)

    # Check whether the snapshot file exists
    assert os.path.exists(shapshot)

    # Test the restore the snapshot
    f2fs(shapshot, output_dir)

    # Check whether the files in the output directory have been restored
    assert os.path.exists(os.path.join(output_dir, "test_file.txt"))
    assert os.path.exists(os.path.join(output_dir, "subdir", "nested_file.txt"))

    # Check the contents of the restored files
    with open(os.path.join(output_dir, "test_file.txt")) as f:
        restored_content = f.read()
        assert restored_content == "This is a test file."

    with open(os.path.join(output_dir, "subdir", "nested_file.txt")) as f:
        restored_content = f.read()
        assert restored_content == "Nested file content."

    # Check the hashes of the restored files
    assert hash(os.path.join(output_dir, "test_file.txt")) == hash(os.path.join(input_dir, "test_file.txt"))
    assert (
        hash(os.path.join(output_dir,
        "subdir",
        "nested_file.txt")) == hash(os.path.join(input_dir,
        "subdir",
        "nested_file.txt"))
    )
