from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader

from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os


PDF_PATH = 'documents/file.pdf'
INDEX_FOLDER = 'model'
OPENAI_TOKEN = 'TOKEN'
vectors_base = None
qa_model = None


template = """
Ваша роль - консультант клиентов.
Ваша задача - отвечать на вопросы клиентов, руководствуясь предложенными фрагментами документов.
Никогда не выдумывайте ответ, если его нет в предложенных фрагментах документов.
Используйте от 3 до 10 предложений. Ваш ответ должен быть краткий и содержательный.
Всегда говори "Спасибо за Ваш вопрос!" в начале ответа.
Используйте только русские слова в своей ответе.
Укажите название главы, где содержится ответ.
Не придумывайте ответ, если его нет в предложенном фрагменте документов.
Предложенных фрагменты документов: {context}
Вопрос клиента: {question}
Ответ на русском языке:"""


class Question(BaseModel):
    content: str
    used_id: int


os.environ['OPENAI_API_KEY'] = OPENAI_TOKEN

app = FastAPI()

@app.get('/')
async def touch():
    return {'response': 'Welcome!'}


@app.post('/question/')
async def get_answer(question: Question):
    global vectors_base, qa_model

    if vectors_base is None:
        return {'answer': 'Пожалуйста, загрузите документ'}
    else:
        return {'answer': qa_model.invoke(question.content)['result']}
    

@app.post('/upload_pdf/')
async def upload_pdf(file: UploadFile):
    global PDF_PATH

    with open(PDF_PATH, 'wb') as pdf:
        pdf.write(file.file.read())

    pdf_text, num_pages = await read_pdf(PDF_PATH)

    await build_model(pdf_text)

    return {
        'status': 200,
        'pdf_name': file.filename,
        'pdf_pages': num_pages,
        'pdf_size': file.size,
    }


async def read_pdf(path: str) -> tuple[str, int]:
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    pdf_text = ''
    for page in pages:
        pdf_text += page.page_content.strip() + f"\n СТРАНИЦА ({page.metadata['page']}) \n\n"
    return pdf_text, len(pages)


async def build_model(content: str):
    global INDEX_FOLDER, vectors_base, qa_model

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
    )

    texts = text_splitter.create_documents([content])[:500]
    vectors_base = FAISS.from_documents(texts, GPT4AllEmbeddings())
    vectors_base.save_local(INDEX_FOLDER)

    qa_model = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        chain_type="stuff",
        retriever=vectors_base.as_retriever(search_kwargs={"k": 10}),
        chain_type_kwargs={"prompt": PromptTemplate(template=template, input_variables=["context", "question"])},
        return_source_documents=True,
    )
