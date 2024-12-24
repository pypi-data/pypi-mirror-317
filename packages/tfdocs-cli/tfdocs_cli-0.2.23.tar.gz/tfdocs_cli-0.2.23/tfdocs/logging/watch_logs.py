import logging
import pickle
import socketserver
from tfdocs.logging import setup_logs

HOST, PORT = "localhost", 1234

setup_logs()

log = logging.getLogger("watch_logs")


def parse_args(subparsers):
    parser = subparsers.add_parser(
        "watch-logs", help="view logs produced by the program in real time"
    )
    parser.set_defaults(func=main)


def main():
    with socketserver.UDPServer((HOST, PORT), LogServerHandler) as server:
        log.info(f"Listening for logs on port {PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt as e:
            log.warn("Exited...")


class LogServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        log_record = logging.makeLogRecord(pickle.loads(data[4:]))
        log.handle(log_record)
        socket.sendto(data.upper(), self.client_address)
