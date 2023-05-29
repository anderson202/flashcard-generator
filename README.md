# flashcard-generator

## Setup

Install SpaCy - https://spacy.io/usage

`pip install requirements.txt`

### Run

`python3.9 generator.py`

## Features
- PDF to flashcards
  - Parse PDF -> Split into chunks -> feed into GPT for flashcards -> combine all flashcards
- Video to flashcards
  - Transcribe video with Whisper API -> ^ same as above
  - or we could just use 'Video Insights' chatgpt plugin


## References
https://platform.openai.com/docs/guides/speech-to-text
https://python.langchain.com/en/latest/modules/indexes/text_splitters/examples/recursive_text_splitter.html
https://www.pinecone.io/learn/chunking-strategies/
https://www.psychic.dev/post/build-a-bot-to-answer-questions-over-documents-with-gpt-and-weaviate
