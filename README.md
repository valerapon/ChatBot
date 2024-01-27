# ChatBot
Сборка: `docker build -t chatbot .`   
Запуск: `docker run -d --name ChatBot -p 80:80 chatbot`  
Тест:
 - по ссылке http://127.0.0.1
 - сделать запрос на http://127.0.0.1/send_message/ с телом
   ```
   {
       'content': '<какой-то текст>'
   }
   ```
   результат
   ```
   {
       'status': 200,
       'result': message.content[::-1],
       'extra': 'Hello, Mans',
    }
   ```
 - есть еще вспомогательная ссылка-дока: http://127.0.0.1/docs – можно узнать про формат запроса.
