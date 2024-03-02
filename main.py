import server
import server as s
import client as c


mode = input("Enter connection mode: ")
while mode.lower() not in ["client", "server"]:
    mode = input("Enter connection mode: ")

if mode == "server":
    s.start_server()
else:
    c.start_client(s.SERVER_IP, s.SERVER_PORT)
