import os
from fastapi import FastAPI
from src import create_logger, check_app, build_base, build_model


os.environ['OPENAI_API_KEY'] = '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'


check_app()
logger = create_logger('main.log')
vectors_base, chunks_dict = build_base()
model = build_model(vectors_base)
app = FastAPI()


@app.get('/')
async def touch():
    logger.info('GET: "/", OK')
    return {'response': 'Welcome!'}


@app.post('/question/')
async def get_answer(question: str):
    logger.info(f'POST: "/question/", question: "{question}"')

    try:
        response =  model.invoke(question)
        answer = response['result']
        source = response['source_documents'][0].page_content
        if source not in chunks_dict or 'К сожалению' in answer or 'нет информации о том' in answer:
            page_name, doc_name, source = ('-1', 'unknown', '')
        else:
            page_name, doc_name = chunks_dict[source]
    except:
        answer = 'Ошибка выполнения, попробуйте снова.'
        source = ''
        page_name = '-1'
        doc_name = 'unknown'
        logger.exception('Error in the QA model.')

    logger.info(f'POST: "/question/", response: "{response}".')
    return {
        'answer': answer,
        'source': source,
        'page_num': page_name,
        'doc_name': doc_name,
    }
