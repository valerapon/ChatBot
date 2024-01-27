# ChatBot
Сборка: `docker build -t chatbot .`   
Запуск: `docker run -d --name ChatBot -p 80:80 chatbot`  
Остановка: `docker stop ChatBot`
Удаление: `docker rm ChatBot`
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

Если перейти по ссылке-доке, можно увидеть запрос:  
```
curl -X 'POST' \
  'http://127.0.0.1/send_message/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "Привет, я крутой чувак"
}'
```  
Response body:  
```
{
  "status": 200,
  "result": "кавуч йотурк я ,тевирП",
  "extra": "Hello, Mans"
}
```

Response headers:  
```
 content-length: 88 
 content-type: application/json 
 date: Sat,27 Jan 2024 17:42:29 GMT 
 server: uvicorn
```
