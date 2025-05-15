from app.rag.ingestion.text_splitter import split_text


def test_split_text():
    text = "This is a sample policy." * 100
    chunks = split_text(text, max_tokens=50)
    assert len(chunks) > 1
    assert all(isinstance(c, str) for c in chunks)
