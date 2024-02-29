import socket
import sys

def proxy_server(webserver, port, conn, addr, data):
    try:
        # 연결을 원격 웹 서버로 전달
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data)

        while True:
            # 원격 서버로부터 데이터 받기
            reply = s.recv(4096)

            if len(reply) > 0:
                # 데이터를 클라이언트로 전달
                conn.sendall(reply)
                # 응답을 캐시에 저장할 수 있도록 추가
                save_cache(data, reply, webserver, port)
            else:
                break

        s.close()
        conn.close()
    except socket.error as err:
        print(err)
        if s:
            s.close()
        if conn:
            conn.close()
        sys.exit(1)

def save_cache(request, response, webserver, port):
    # 여기서는 간단하게 캐시를 파일로 저장합니다.
    filename = webserver.replace(".", "_") + "_" + str(port) + ".txt"
    with open(filename, "wb") as cache_file:
        cache_file.write(request)
        cache_file.write(response)

def main():
    try:
        # 로컬 호스트와 포트 설정
        host = '127.0.0.1'
        port = 8888

        # 소켓 생성
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(10)

        print("Proxy server is listening on port", port)

        while True:
            # 연결 수락
            conn, addr = s.accept()
            data = conn.recv(4096)
            # 클라이언트 요청 분석
            if not data:
                continue
            try:
                first_line = data.decode().split('\n')[0]
            except UnicodeDecodeError:
                print("Failed to decode data")
                continue
            url = first_line.split(' ')[1]
            http_pos = url.find("://")
            if http_pos == -1:
                temp = url
            else:
                temp = url[(http_pos + 3):]

            port_pos = temp.find(":")

            webserver_pos = temp.find("/")
            if webserver_pos == -1:
                webserver_pos = len(temp)

            webserver = ""
            port = -1
            if port_pos == -1 or webserver_pos < port_pos:
                port = 80
                webserver = temp[:webserver_pos]
            else:
                port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
                webserver = temp[:port_pos]

            proxy_server(webserver, port, conn, addr, data)

    except Exception as e:
        print(e)
        if s:
            s.close()
        sys.exit(1)

if __name__ == "__main__":
    main()
