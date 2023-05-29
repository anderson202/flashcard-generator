import os
import openai
from pdfminer.high_level import extract_text
import spacy
from spacy.lang.en import English
from langchain.text_splitter import RecursiveCharacterTextSplitter

openai.api_key = os.getenv("OPENAI_API_KEY")
nlp = spacy.load("en_core_web_sm")

context = "You're an assistant that will create flashcards based on provided text. Only use the information provided and nothing else. If there is no valid information to generate cards with, simply return None. Otherwise, return strictly in format of question followed by semicolon followed by answer in double quotes. Do not prefix with numbers. For example, Question;\"Answer\""

def summarize_text(text):
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": 'Generate anywhere between 10-30 flashcards (up to your discretion on how much content can actually be used) for the following text: ' + text}
      ],
      temperature=0.3, 
      top_p=1, 
      frequency_penalty=0,
      presence_penalty=1
  )
  return response["choices"][0]["message"]["content"]

def recursive_split(text):
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2500,
    chunk_overlap  = 100,
    length_function = len,
  )
  res = text_splitter.split_text(text)
  return res

def simple_text_split(text):
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
    page_numbers = (start_page, end_page) if (start_page is not None and end_page is not None) else None
    return extract_text(file_path, page_numbers=page_numbers)

def write_string_to_file(file_path, content):
    f = open(file_path, "w")
    f.write(content)
    f.close()

# Provide the path to your PDF file
pdf_file_path = 'pdf/sdlc.pdf'

# Call the function to extract paragraphs from the specified pages of the PDF file
text = extract_text_from_pdf(pdf_file_path)

paragraphs = recursive_split(text)
print(paragraphs)
print(len(paragraphs))

flashcards = []
for paragraph in paragraphs:
   output = summarize_text(paragraph)
   flashcards.append(output)
   
write_string_to_file('cards/test4.txt', "\n".join(flashcards))
