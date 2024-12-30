import time

from AndroidTraceTool.core.micro_server import TraceSocket

if __name__ == '__main__':

    trace_socket = TraceSocket("849f580b")
    time.sleep(1)
    trace_socket.start_trace("test")
    time.sleep(1)
    trace_socket.stop_trace()
    trace_socket.stop_socket()