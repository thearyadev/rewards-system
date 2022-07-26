from __future__ import annotations

from util import WebServer, Finances

if __name__ == '__main__':
    finances = Finances() #init finances
    finances.load(itemJSON="./data/ITEMS") # path to item file
    server = WebServer(finances=finances) # init web server

    server.run(debug=True, host="0.0.0.0", port=80)
