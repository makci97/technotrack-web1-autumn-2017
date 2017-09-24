# -*- coding: utf-8 -*-
import os
import socket

def parse_request(request):
    """Получает метод, путь и содержимое заголовка User-Agent, переданные в запросе"""
    headers = {line.split(" ")[0] : " ".join(line.split(" ")[1:])
               for line in request.split("\r\n")[1:]}
    method, path = request.split(" ")[:2]
    return method, path, headers["User-Agent:"]

def create_response(code, body=""):
    """Создает ответ на запрос

    Parameters
    ----------
    code : string
        Код ответа
    body : string
        Тело ответа
    """
    return "HTTP/1.1 " + code + "\n" + "Content-Type: text/html" + "\n\n" + body

def create_body(html_body):
    """Создает тело ответа -- html-страницу

    Parameters
    ----------
    html_body : string
        Html-код тела страницы
    """
    body = "<html><head></head><body>" + html_body + "</body></html>"
    return body

def get_response(request):
    method, path, user_agent = parse_request(request)

    if method != "GET":
        return create_response("404 Not found", create_body("File not found"))

    # обработка /
    if path == "/":
        html_body = "Hello mister!<br>You are: " + user_agent
        return create_response("200 OK", create_body(html_body))

    # обработка /media/
    if path == "/media/" or path == "/media":
        html_body = "<ul>"
        for file in os.listdir("files"):
            html_body += "<li>" + file + "</li>"
        html_body += "</ul>"
        return create_response("200 OK", create_body(html_body))

    # обработка /media/file
    splited_path = path.split("/")
    if (splited_path[1] == "media"
        and len(splited_path) == 3):
        file_name = splited_path[2]
        try:
            with open("./files/" + file_name, "r") as file:
                html_body = file.read().encode("utf-8")
                return create_response("200 OK", create_body(html_body))
        except:
            return create_response("404 Not found", create_body("Page not found"))

    # обработка /test/
    if path == "/test/" or path == "/test":
        return create_response("200 OK", create_body(request))

    # обработка остальных запросов
    return create_response("404 Not found", create_body("Page not found"))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))     # связываем сокет с данными хостом и портом
server_socket.listen(1)  # устанавливаем сокет в режим прослушивания с максимальным количеством подключений в очереди

print('Started')

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print('Got new client ', client_socket.getsockname())  # при подлючении нового клиента пишем имя его сокета
        request_string = client_socket.recv(2048)  # получаем строку запроса размером не более 2048 байт
        client_socket.send(get_response(request_string))  # отправляем клиенту строку ответа на запрос
        client_socket.close()   # закрываем соединение с данным клиентом
    except KeyboardInterrupt:   # исключение прерывания программы
        print('Stopped')
        server_socket.close()  # закрываем серверный сокет и тем самым останавливаем получение и обработку запросов
        exit()
