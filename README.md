# ChatBot
Сборка: `docker build -t chatbot .`   
Запуск: `docker run -d --name ChatBot -p 80:80 chatbot`   
Остановка: `docker stop ChatBot`  
Удаление: `docker rm ChatBot`  
Тест:  
 - по ссылке http://127.0.0.1;
 - дока: http://127.0.0.1/docs;
 - get-запрос на http://127.0.0.1/ – проверка работы;
 - post-запрос на http://127.0.0.1/upload_pdf/ – загрузить **pdf**-домекумент:
   ```
     'http://127.0.0.1:8000/upload_pdf/' \
     -H 'accept: application/json' \
     -H 'Content-Type: multipart/form-data' \
     -F 'file=@mypdffile.pdf;type=application/pdf'
   ```
   результат
   ```
   {
     "status": 200,
     "pdf_name": "mypdffile.pdf",
     "pdf_pages": 132,
     "pdf_size": 778435
   }
   ```
 - post-запрос на http://127.0.0.1/question/ – задать вопрос:
   ```
   curl -X 'POST' \
     'http://127.0.0.1:8000/question/' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
     "content": "О чем этот документ?",
     "used_id": 0
   }'
   ```
   результат:
   ```
   {
     "answer": "Спасибо за Ваш вопрос! Этот документ содержит информацию о возможности частичного досрочного погашения кредита, а также о последствиях полного и неполного погашения регулярных платежей. Также в документе описаны условия совершения переводов с использованием номера сотового телефона или номера карты."
   }
   ```
