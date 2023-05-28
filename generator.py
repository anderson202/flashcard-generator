import os
import openai
from pdfminer.high_level import extract_text
import spacy
from spacy.lang.en import English


openai.api_key = os.getenv("OPENAI_API_KEY")

context = "Create flashcards for "

def summarize_text(text):
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=[
        {"role": "system", "content": "You're an assistant that will create flashcards based on provided text. Only use the information provided and nothing else. If there is no valid information to generate cards with, simply return an empty string. Otherwise, return in format of question followed by semicolon followed by answer in double quotes. For example, Question;\"Answer\""},
        {"role": "user", "content": 'Generate flashcards for the following: ' + text}
      ],
      temperature=0.3, 
      top_p=1, 
      frequency_penalty=0,
      presence_penalty=1
  )
  return response["choices"][0]["message"]["content"]

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    return text.replace('\n', ' ')

def text_to_chunks(text):
  chunks = [[]]
  chunk_total_words = 0

  sentences = nlp(text)

  for sentence in sentences.sents:
    chunk_total_words += len(sentence.text.split(" "))

    if chunk_total_words > 2700:
      chunks.append([])
      chunk_total_words = len(sentence.text.split(" "))

    chunks[len(chunks)-1].append(sentence.text)
  
  return chunks

def extract_text_from_pdf(file_path, start_page=None, end_page=None):
    # Determine the range of pages to extract
    page_numbers = (start_page, end_page) if (start_page is not None and end_page is not None) else None

    # Extract text from the PDF file
    return extract_text(file_path, page_numbers=page_numbers)

def write_string_to_file(file_path, content):
    f = open(file_path, "w")
    f.write(content)
    f.close()

# Provide the path to your PDF file
pdf_file_path = 'pdf/sdlc.pdf'

# Call the function to extract paragraphs from the specified pages of the PDF file
text = extract_text_from_pdf(pdf_file_path, 0, 1)

chunks = text_to_chunks(preprocess_text(text))

print(chunks)

output = summarize_text(text)
print(output)

write_string_to_file('cards/test.txt', output)
