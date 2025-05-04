from journal_ai.journal.tags import generate_tags


def test_generate_tags():
    """Test the generate_tags function."""
    content = "This is a test journal entry with tags @journal @writing @test"
    expected_tags = ["journal", "writing", "test"]
    assert generate_tags(content) == expected_tags


def test_generate_tags_no_tags():
    """Test the generate_tags function with no tags."""
    content = "This is a test journal entry with no tags."
    expected_tags = []
    assert generate_tags(content) == expected_tags


def test_generate_tags_no_content():
    """Test the generate_tags function with no content."""
    content = ""
    expected_tags = []
    assert generate_tags(content) == expected_tags


def test_generate_tags_two_tags():
    """Test the generate_tags function with two tags."""
    content = "@tag1 @tag2"
    expected_tags = ["tag1", "tag2"]
    assert generate_tags(content) == expected_tags


def test_email_in_content():
    """Test the generate_tags function with an email in the content."""
    content = "The email is test@test.com."
    expected_tags = []
    assert generate_tags(content) == expected_tags
