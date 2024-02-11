from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src import create_logger


def build_model(vectors_base):
    logger = create_logger('build_model.log')
    logger.info('Start to creating QA model.')

    template = """
    Ваша роль - консультант клиентов.
    Ваша задача - отвечать на вопросы клиентов, руководствуясь предложенными фрагментами документов.
    Никогда не выдумывайте ответ, если его нет в предложенных фрагментах документов.
    Используйте от 3 до 10 предложений. Ваш ответ должен быть краткий и содержательный.
    Всегда говори "Спасибо за Ваш вопрос!" в начале ответа.
    Используйте только русские слова в своей ответе.
    Ответ на вопрос содержится в документах, найди его и напиши.
    Предложенных фрагменты документов: {context}
    Вопрос клиента: {question}
    Ответ на русском языке:"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"],
    )
    llm = ChatOpenAI(
        model='gpt-4',
        temperature=0,
        # max_tokens=4000
    )

    model = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectors_base.as_retriever(search_kwargs={'k': 3}),
        chain_type_kwargs={'prompt': prompt},
        return_source_documents=True,
    )

    logger.info('The model was created. Success.')
    return model