from datetime import datetime

from utils.generic_document import AbstractBaseDocument


def test_AbstractBaseStakeholder():
    document = AbstractBaseDocument(doc_title="fake_doc_title")

    assert document.doc_title == "fake_doc_title"
    assert isinstance(document.time_created, datetime)
