import os
import re
import pickle
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src import create_logger


def read_documents(logger):
    full_text = []
    all_pages = []
    docs = os.listdir('docs')
    for doc in docs:
        loader = PyPDFLoader(f'docs/{doc}')
        for i, page in enumerate(loader.load()):
            full_text.append(page.page_content.strip() + f'@@pageid_{i + 1}_{doc}')
    logger.info('Documents were red. Success.')
    return '\n\n'.join(full_text)


def make_chunks(logger):
    text = read_documents(logger)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100,
    )
    chunks = splitter.create_documents([text])
    logger.info('Chunks were build. Success.')

    chunks_dict = {}
    for i in range(len(chunks)):
        chunks_dict[chunks[i].page_content] = ('-1', 'unknown')
        for j in range(i, len(chunks)):
            if '@@pageid_' in chunks[j].page_content:
                pageid = re.findall('@@pageid_(\d+)_(.+?\.pdf)', chunks[j].page_content)
                chunks_dict[chunks[i].page_content] = pageid[0]
                break
    return chunks, chunks_dict


def build_index(logger):
    chunks, chunks_dict = make_chunks(logger)
    embedder = OpenAIEmbeddings()
    vectors_base = FAISS.from_documents([chunks[0]], embedder)

    for i in range(1, len(chunks)):
        time.sleep(1)
        new_emb = FAISS.from_documents([chunks[i]], embedder)
        vectors_base.merge_from(new_emb)
        logger.info(f'Doc {i} embedded into {new_emb.docstore._dict.keys()}. Success.')
        
    vectors_base.save_local('index')
    with open('index/chunks.pkl', 'wb') as file:
        pickle.dump(chunks_dict, file)

    logger.info('Index base was created. Success.')
    return vectors_base, chunks_dict


def build_base():
    logger = create_logger('build_base.log')
    logger.info('Start to building base.')

    if len(os.listdir('index')) == 0:
        vectors_base, chunks_dict = build_index(logger)
    else:
        embedder = OpenAIEmbeddings()
        vectors_base = FAISS.load_local('index', embedder)
        with open('index/chunks.pkl', 'rb') as file:
            chunks_dict = pickle.load(file)
    
    logger.info('The base was loaded. Success.')
    return vectors_base, chunks_dict
