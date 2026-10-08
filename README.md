# Codescape Bank Document Parser

`codescape-bank-parse` is a shared Python library for identifying bank documents
and extracting classification metadata. It currently reads PDF files and supports
account statements from comdirect, ING and Scalable Capital. Scalable Capital
documents also include contract notes and dividend corporate actions.

The library is intended for use in document-routing and portfolio-tracking
applications. Support for other input formats can be added as needed.

## Usage

```python
from codescape.parse import parse_document

metadata = parse_document("statement.pdf")
if metadata is not None:
    print(metadata.bank, metadata.category)
```

`parse_document` also accepts a `pathlib.Path`, `bytes` or an in-memory
`io.BytesIO` PDF source. It returns `None` when the document is empty or no
registered classifier recognises it. Classifiers can be registered with a
`ClassifierRegistry` and passed to `parse_document` when custom dispatch is needed.
