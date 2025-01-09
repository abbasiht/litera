import unittest
from unittest.mock import patch, mock_open
import os
import tempfile
from pathlib import Path
from litera import Block, FileBlock, CodeBlock, DocumentationBlock, Container
from litera import make_block, parse_files


class TestBlock(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.temp_file.write(b"Temporary file content")
        self.temp_file.close()

        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary file and directory after tests
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_valid_file(self):
        # Test with a valid file
        block = Block("Sample content", self.temp_file.name)
        self.assertEqual(block.content, "Sample content")
        self.assertEqual(
            block.container, os.path.basename(self.temp_file.name).rsplit(".", 1)[0]
        )

    def test_directory_as_container(self):
        # Test with a directory instead of a file
        with self.assertRaises(ValueError) as context:
            Block("Directory content", self.temp_dir)

    def test_non_existent_file(self):
        # Test with a non-existent file
        non_existent_file = "/path/to/nonexistent/file.txt"
        with self.assertRaises(FileNotFoundError) as context:
            Block("Missing file content", non_existent_file)

    def test_file_without_extension(self):
        # Test with a valid file without an extension
        temp_file_no_ext = tempfile.NamedTemporaryFile(delete=False)
        temp_file_no_ext.close()
        try:
            block = Block("Content without extension", temp_file_no_ext.name)
            self.assertEqual(block.container, os.path.basename(temp_file_no_ext.name))
        finally:
            os.unlink(temp_file_no_ext.name)

    def test_file_with_multiple_dots(self):
        # Test with a file name containing multiple dots
        temp_file_multi_dot = tempfile.NamedTemporaryFile(
            delete=False, prefix="file.name.with.dots.", suffix=".txt"
        )
        temp_file_multi_dot.close()
        try:
            block = Block("Content with dots", temp_file_multi_dot.name)
            expected_name = os.path.basename(temp_file_multi_dot.name).rsplit(".", 1)[0]
            self.assertEqual(block.container, expected_name)
        finally:
            os.unlink(temp_file_multi_dot.name)


class TestFileBlock(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.temp_file.write(b"Sample content")
        self.temp_file.close()

        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary file and directory after tests
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_valid_fileblock(self):
        # Test initialization with valid arguments
        content = "This is a block of content."
        container = self.temp_file.name
        language = "Python"
        name = os.path.join(self.temp_dir, "file.txt")

        file_block = FileBlock(content, container, language, name)

        # Assert the attributes are correctly set
        self.assertEqual(file_block.content, content)
        self.assertEqual(
            file_block.container, os.path.basename(container).rsplit(".", 1)[0]
        )
        self.assertEqual(file_block.language, language)
        self.assertEqual(file_block.location, name)
        self.assertEqual(file_block.name, os.path.basename(name).rsplit(".", 1)[0])
        self.assertEqual(file_block.type, "file")
        self.assertEqual(file_block.calling, [])
        self.assertEqual(file_block.called_by, [])
        self.assertEqual(file_block.calling_name, "")

    def test_name_without_extension(self):
        # Test behavior when 'name' does not contain a file extension
        with self.assertRaises(ValueError):
            FileBlock("Content", self.temp_file.name, "Python", "file")

    def test_directory_as_name(self):
        # Test behavior when a directory is passed as the 'name'
        with self.assertRaises(ValueError):
            FileBlock("Content", self.temp_file.name, "Python", self.temp_dir)


class TestCodeBlock(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.temp_file.write(b"Sample content")
        self.temp_file.close()

        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary file and directory after tests
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_valid_codeblock(self):
        # Test initialization with valid arguments
        content = "This is a block of code."
        container = self.temp_file.name
        language = "Python"
        name = os.path.join(self.temp_dir, "script.py")

        code_block = CodeBlock(content, container, language, name)

        # Assert the attributes are correctly set
        self.assertEqual(code_block.content, content)
        self.assertEqual(
            code_block.container, os.path.basename(container).rsplit(".", 1)[0]
        )
        self.assertEqual(code_block.language, language)
        self.assertEqual(code_block.location, name)
        self.assertEqual(code_block.name, os.path.basename(name).rsplit(".", 1)[0])
        self.assertEqual(code_block.type, "code")  # Ensure the type is "code"
        self.assertEqual(code_block.calling, [])
        self.assertEqual(code_block.called_by, [])
        self.assertEqual(code_block.calling_name, "")


class TestDocumentationBlock(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.temp_file.write(b"Sample content")
        self.temp_file.close()

        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary file and directory after tests
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_valid_documentationblock(self):
        # Test initialization with valid arguments
        content = "This is a documentation block."
        container = self.temp_file.name
        documentation_block = DocumentationBlock(content, container)

        # Assert the attributes are correctly set
        self.assertEqual(documentation_block.content, content)
        self.assertEqual(
            documentation_block.container, os.path.basename(container).rsplit(".", 1)[0]
        )
        self.assertEqual(documentation_block.type, "doc")  # Ensure the type is "doc"


class TestContainer(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.temp_file.write(b"Sample content")
        self.temp_file.close()

        # Create a Container for testing
        self.container = Container(self.temp_file.name)

    def tearDown(self):
        # Clean up the temporary file after tests
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_initialization(self):
        # Test initialization of the container
        self.assertEqual(
            self.container.name, os.path.basename(self.temp_file.name).rsplit(".", 1)[0]
        )
        self.assertEqual(self.container.blocks, [])
        self.assertEqual(self.container.code_dir, "")
        self.assertEqual(self.container.doc_dir, "")
        self.assertEqual(self.container.title, "")
        self.assertEqual(self.container.execute, [])
        self.assertEqual(self.container.local_link, [])
        self.assertEqual(self.container.web_link, [])
        self.assertEqual(self.container.local_script, [])
        self.assertEqual(self.container.web_script, [])

    def test_add_block(self):
        # Test adding a Block to the container
        block = Block("Sample content", self.temp_file.name)
        self.container.add(block)

        # Assert the block is added to the container
        self.assertEqual(len(self.container.blocks), 1)
        self.assertEqual(self.container.blocks[0], block)

    def test_set_title(self):
        # Test setting the title of the container
        title = "Sample Container"
        self.container.set_title(title)

        # Assert the title is set correctly
        self.assertEqual(self.container.title, title)

    def test_add_local_link(self):
        # Test adding a local link
        link_type = "type1"
        link_address = "http://localhost"
        self.container.add_llink(link_type, link_address)

        # Assert the link is added to the local_link list
        self.assertEqual(len(self.container.local_link), 1)
        self.assertEqual(self.container.local_link[0], [link_type, link_address])

    def test_add_web_link(self):
        # Test adding a web link
        link_type = "type2"
        link_address = "http://example.com"
        self.container.add_wlink(link_type, link_address)

        # Assert the link is added to the web_link list
        self.assertEqual(len(self.container.web_link), 1)
        self.assertEqual(self.container.web_link[0], [link_type, link_address])


class TestContainer(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.temp_file.write(b"Sample content")
        self.temp_file.close()

        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

        # Create a temporary file for testing links
        self.temp_link_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        self.temp_link_file.write(b"Image content")
        self.temp_link_file.close()

    def tearDown(self):
        # Clean up the temporary files and directories after tests
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
        if os.path.exists(self.temp_link_file.name):
            os.unlink(self.temp_link_file.name)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_valid_container(self):
        # Test initialization with a valid file
        container = Container(self.temp_file.name)
        self.assertEqual(
            container.name, os.path.basename(self.temp_file.name).rsplit(".", 1)[0]
        )

    def test_directory_as_container(self):
        # Test behavior when a directory is passed as the container
        with self.assertRaises(ValueError):
            Container(self.temp_dir)

    def test_non_existent_container(self):
        # Test behavior when a non-existent file is passed as the container
        non_existent_file = "non_existent_file.txt"
        with self.assertRaises(FileNotFoundError):
            Container(non_existent_file)

    def test_add_block(self):
        # Test adding a block to the container
        container = Container(self.temp_file.name)
        content = "This is some content"
        block = Block(content, self.temp_file.name)  # Pass content and container
        container.add(block)
        self.assertEqual(len(container.blocks), 1)

    def test_add_llink_valid(self):
        # Test adding a local link when the file exists
        container = Container(self.temp_file.name)
        container.add_llink("image", self.temp_link_file.name)
        self.assertEqual(len(container.local_link), 1)

    def test_add_llink_invalid(self):
        # Test adding a local link when the file does not exist
        container = Container(self.temp_file.name)
        with self.assertRaises(FileNotFoundError):
            container.add_llink("image", "non_existent_image.jpg")

    def test_add_wlink(self):
        # Test adding a web link to the container
        container = Container(self.temp_file.name)
        container.add_wlink("CSS", "https://example.com/style.css")
        self.assertEqual(len(container.web_link), 1)

    def test_set_code_dir_valid(self):
        # Tests if the set_code_dir method works with a valid directory ending with '/'
        valid_dir = "code/"
        container = Container(self.temp_file.name)
        container.set_code_dir(valid_dir)
        self.assertEqual(container.code_dir, valid_dir)

    def test_set_code_dir_invalid(self):
        # Tests if a ValueError is raised when the directory does not end with '/'
        invalid_dir = "code"
        container = Container(self.temp_file.name)
        with self.assertRaises(ValueError) as context:
            container.set_code_dir(invalid_dir)

    def test_set_code_dir_empty(self):
        # Test that no action is taken when the code directory is an empty string
        container = Container(self.temp_file.name)
        container.set_code_dir("")
        self.assertEqual(container.doc_dir, "")

    def test_set_doc_dir_valid(self):
        # Tests if the set_doc_dir method works with a valid directory ending with '/'
        valid_dir = "docs/"
        container = Container(self.temp_file.name)
        container.set_doc_dir(valid_dir)
        self.assertEqual(container.doc_dir, valid_dir)

    def test_set_doc_dir_invalid(self):
        # Tests if a ValueError is raised when the directory does not end with '/'
        invalid_dir = "docs"
        container = Container(self.temp_file.name)
        with self.assertRaises(ValueError) as context:
            container.set_doc_dir(invalid_dir)

    def test_set_doc_dir_empty(self):
        # Test that no action is taken when the doc directory is an empty string
        container = Container(self.temp_file.name)
        container.set_doc_dir("")
        self.assertEqual(container.doc_dir, "")


class TestMakeBlock(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.temp_file.write(b"Some content")  # Write content to the file
        self.temp_file.close()  # Close the file so it can be used

    def tearDown(self):
        # Clean up the temporary file after tests
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_make_doc_block(self):
        # Test creating a documentation block
        block = make_block("doc", "This is documentation content", self.temp_file.name)
        self.assertIsInstance(block, DocumentationBlock)

    def test_make_file_block(self):
        # Test creating a file block
        block = make_block(
            "file",
            "This is a file content",
            self.temp_file.name,
            language="Python",
            name="file.py",
        )
        self.assertIsInstance(block, FileBlock)

    def test_make_code_block(self):
        # Test creating a code block
        block = make_block(
            "code",
            "This is code content",
            self.temp_file.name,
            language="Python",
            name="code.py",
        )
        self.assertIsInstance(block, CodeBlock)

    def test_invalid_block_type(self):
        # Test that an invalid block type raises a ValueError
        with self.assertRaises(ValueError):
            make_block("invalid", "Some content", self.temp_file.name)


class TestParseFiles(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.temp_file.close()

        self.second_temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.second_temp_file.close()

    def tearDown(self):
        # Clean up the temporary file after tests
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

        if os.path.exists(self.second_temp_file.name):
            os.unlink(self.second_temp_file.name)

    def test_empty_file(self):
        # Test that a ValueError is raised when an empty file is encountered.
        with self.assertRaises(ValueError):
            parse_files([self.temp_file.name])

    def test_improper_doc_dir(self):
        # Test that ValueError is raised when the metadata is improper
        with open(self.temp_file.name, "w") as file:
            file.write("@documentation_folder{docs/html}")  # Write improper metadata

        with self.assertRaises(ValueError):
            parse_files([self.temp_file.name])

    def test_doc_dir(self):
        # Testing to ensure doc_dir is parsed correctly in all conditions

        # Condition 1: Metadata does not appear
        with open(self.temp_file.name, "w") as file:
            file.write("just so the file isn't empty")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.doc_dir, "")

        # Condition 2: Metadata appears once
        with open(self.temp_file.name, "w") as file:
            file.write("@documentation_folder{docs/}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.doc_dir, "docs/")

        # Condition 3: Metadata appears multiple times
        with open(self.temp_file.name, "w") as file:
            file.write("@documentation_folder{docs/}\n@documentation_folder{new_docs/}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.doc_dir, "new_docs/")

    def test_improper_code_dir(self):
        # Test that ValueError is raised when the metadata is improper
        with open(self.temp_file.name, "w") as file:
            file.write("@code_folder{code}")  # Write improper metadata

        with self.assertRaises(ValueError):
            parse_files([self.temp_file.name])

    def test_code_dir(self):
        # Testing to ensure code_dir is parsed correctly in all conditions

        # Condition 1: Metadata does not appear
        with open(self.temp_file.name, "w") as file:
            file.write("just so the file isn't empty")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.code_dir, "")

        # Condition 2: Metadata appears once
        with open(self.temp_file.name, "w") as file:
            file.write("@code_folder{code/}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.code_dir, "code/")

        # Condition 3: Metadata appears multiple times
        with open(self.temp_file.name, "w") as file:
            file.write("@code_folder{code/}\n@code_folder{new_code/}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.code_dir, "new_code/")

    def test_title(self):
        # Testing to ensure title is parsed correctly in all conditions

        # Condition 1: Metadata does not appear
        with open(self.temp_file.name, "w") as file:
            file.write("just so the file isn't empty")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.title, "")

        # Condition 2: Metadata appears once
        with open(self.temp_file.name, "w") as file:
            file.write("@title{First Title}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.title, "First Title")

        # Condition 3: Metadata appears multiple times
        with open(self.temp_file.name, "w") as file:
            file.write("@title{First Title}\n@title{Second Title}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.title, "Second Title")

    def test_execute(self):
        # Testing to ensure execute is parsed correctly in all conditions

        # Condition 1: Metadata does not appear
        with open(self.temp_file.name, "w") as file:
            file.write("no execute metadata here")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.execute, [])

        # Condition 2: Metadata appears once
        with open(self.temp_file.name, "w") as file:
            file.write("@execute_end{command1}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.execute, ["command1"])

        # Condition 3: Metadata appears multiple times
        with open(self.temp_file.name, "w") as file:
            file.write("@execute_end{command1}\n@execute_end{command2}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.execute, ["command1", "command2"])

    def test_local_script(self):
        # Testing to ensure local_script is parsed correctly in all conditions

        # Condition 1: Metadata does not appear
        with open(self.temp_file.name, "w") as file:
            file.write("no local_script metadata here")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.local_script, [])

        # Condition 2: Metadata appears once
        with open(self.temp_file.name, "w") as file:
            file.write("@local_script{script1}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.local_script, ["script1"])

        # Condition 3: Metadata appears multiple times
        with open(self.temp_file.name, "w") as file:
            file.write("@local_script{script1}\n@local_script{script2}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.local_script, ["script1", "script2"])

    def test_web_script(self):
        # Testing to ensure web_script is parsed correctly in all conditions

        # Condition 1: Metadata does not appear
        with open(self.temp_file.name, "w") as file:
            file.write("no web_script metadata here")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.web_script, [])

        # Condition 2: Metadata appears once
        with open(self.temp_file.name, "w") as file:
            file.write("@web_script{script1}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.web_script, ["script1"])

        # Condition 3: Metadata appears multiple times
        with open(self.temp_file.name, "w") as file:
            file.write("@web_script{script1}\n@web_script{script2}")

        my_dict = parse_files([self.temp_file.name])
        container = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]
        self.assertEqual(container.web_script, ["script1", "script2"])

    def testing_blocks(self):
        # Create and write content to the first temporary file
        with open(self.temp_file.name, "w") as file:
            file.write(
                """## Example Usage\n``` python main.py\ndef main():\n    print("hello world")\nif __name__ == "__main__":\n    @call{main2}\n```\n\nThis is just to showcase how indentation works with the calling command\n```python main2\nmain()\n```"""
            )

        # Create a second temporary file
        with open(self.second_temp_file.name, "w") as file:
            file.write(
                """## Another Example\n``` python script.py\ndef another_function():\n    return "goodbye"\n```\n\nAnother block of code\n```python another\nanother_function()\n```"""
            )

        # Parse both files
        my_dict = parse_files([self.temp_file.name, self.second_temp_file.name])

        # Validate the first container
        container1 = my_dict[os.path.basename(self.temp_file.name).rsplit(".", 1)[0]]

        # Assertions to validate block parsing for the first file
        self.assertIn("blocks", dir(container1))
        self.assertIsInstance(container1.blocks, list)
        self.assertEqual(
            len(container1.blocks), 4
        )  # Total number of blocks should be 4

        # Categorize blocks by type for the first file
        documentation_blocks1 = [
            block for block in container1.blocks if block.type == "doc"
        ]
        file_blocks1 = [block for block in container1.blocks if block.type == "file"]
        code_blocks1 = [block for block in container1.blocks if block.type == "code"]

        # Check counts for the first file
        self.assertEqual(len(documentation_blocks1), 2)  # Two documentation blocks
        self.assertEqual(len(file_blocks1), 1)  # One file block
        self.assertEqual(len(code_blocks1), 1)  # One code block

        # Validate the content of the blocks for the first file
        self.assertEqual(documentation_blocks1[0].content.strip(), "## Example Usage")
        self.assertEqual(file_blocks1[0].content.strip().startswith("def main()"), True)
        self.assertEqual(code_blocks1[0].content.strip(), "main()")

        # Validate the second container
        container2 = my_dict[
            os.path.basename(self.second_temp_file.name).rsplit(".", 1)[0]
        ]

        # Assertions to validate block parsing for the second file
        self.assertIn("blocks", dir(container2))
        self.assertIsInstance(container2.blocks, list)
        self.assertEqual(len(container2.blocks), 4)

        # Categorize blocks by type for the second file
        documentation_blocks2 = [
            block for block in container2.blocks if block.type == "doc"
        ]
        file_blocks2 = [block for block in container2.blocks if block.type == "file"]
        code_blocks2 = [block for block in container2.blocks if block.type == "code"]

        # Check counts for the second file
        self.assertEqual(len(documentation_blocks2), 2)  # One documentation block
        self.assertEqual(len(file_blocks2), 1)  # One file block
        self.assertEqual(len(code_blocks2), 1)  # One code block

        # Validate the content of the blocks for the second file
        self.assertEqual(documentation_blocks2[0].content.strip(), "## Another Example")
        self.assertEqual(
            file_blocks2[0].content.strip().startswith("def another_function()"), True
        )
        self.assertEqual(code_blocks2[0].content.strip(), "another_function()")

        # Clean up the second temporary file


if __name__ == "__main__":
    unittest.main()
