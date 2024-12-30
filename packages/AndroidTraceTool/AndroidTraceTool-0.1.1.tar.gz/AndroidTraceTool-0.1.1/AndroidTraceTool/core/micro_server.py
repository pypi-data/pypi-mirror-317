import datetime
import os
import socket
import struct
import threading
import time
from typing import Dict

from adbutils import AdbDevice, adb

from AndroidTraceTool.utils._print_util import print_info, print_success, print_error, print_warning


class TraceSocket:
    PERF_TEST_MAIN = "com.miui.performancetest.Main"

    device_socket_dict: Dict[str, "TraceSocket"] = dict()

    def __init__(self, device):
        self.__recent_operation_name = None
        self.__trace_cookie = None
        self.__device = self.__init_adb_device(device)
        self.__config_adb_forward()
        self.__socket = None
        self.__running = True
        # 启动心跳检测线程
        self.__heartbeat_thread = threading.Thread(target=self.__heartbeat_check)
        self.__heartbeat_thread.start()
        # sleep 2 s to ensure server start
        time.sleep(2)

    def __config_adb_forward(self):
        self.__forward(18000, 19000)
        self.__start_performance_test_helper_process()
        pass

    def __check_process_exit(self, process):
        result = self.__device.shell(f"ps -df | grep {process}")
        print_info(result)
        is_exist = False
        for line in result.split("\n"):
            if not "grep" in line:
                is_exist = True
        return is_exist

    def __start_performance_test_helper_process(self):
        helper_dex_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "binaries", "miui_performance_helper.dex")
        os.system(f"adb -s {self.__device.serial} push {helper_dex_path} '/data/local/tmp/'")
        os.system(
            f"adb -s {self.__device.serial} shell app_process -Djava.class.path=/data/local/tmp/miui_performance_helper.dex /system/bin com.miui.performancetest.Main &")
        while not self.__check_process_exit(self.PERF_TEST_MAIN):
            time.sleep(1)

    def __stop_performance_test_helper_process(self):
        pid = self.get_process_pid(self.PERF_TEST_MAIN)
        self.__device.shell(f"kill -9 {pid}")
        while self.__check_process_exit(self.PERF_TEST_MAIN):
            print_info(f"{self.PERF_TEST_MAIN} 仍存在等待1s")
            # 可能存在多个，所以开始测试
            pid = self.get_process_pid(self.PERF_TEST_MAIN)
            self.__device.shell(f"kill {pid}")
            time.sleep(1)

    def get_process_pid(self, process):
        result = self.__device.shell(f"ps -df | grep {process}")
        for line in result.split("\n"):
            if not "grep" in line:
                pid = line.split()[1]
                return pid
        return None

    @staticmethod
    def __init_adb_device(device):
        if isinstance(device, AdbDevice):
            return device
        elif isinstance(device, str):
            devices = adb.device_list()
            for d in devices:
                print_info(f"find one device {d.serial}")
                if d.serial == device:
                    return d
            else:
                raise Exception("Unknown device")
        else:
            raise Exception("Unknown device")

    def __check_forward_exist(self, local_port, remote_port):
        """
        检查指定forward是否存在
        :param local_port: 本地端口
        :param remote_port: 远程端口
        :return:
        """
        forward_list = self.__device.forward_list()
        for forward_list in forward_list:
            if f"tcp:{local_port}" == forward_list.local and f"tcp:{remote_port}" == forward_list.remote:
                return True
        return False

    def __forward(self, local_port, remote_port):
        """
        执行adb forward  <local> <remote>
        :param local_port: 主机上的端口
        :param remote_port: 设备上的端口
        :return:
        """
        if self.__check_forward_exist(local_port, remote_port):
            print_info("已存在指定forward，直接返回")
            return
        os.system(f"adb -s {self.__device.serial} forward tcp:{local_port} tcp:{remote_port}")
        while not self.__check_forward_exist(local_port, remote_port):
            print_info("等待forward执行成功")
            time.sleep(1)

    def _send_utf8_data(self, data):
        """
        按照类似Java writeUTF的格式发送UTF-8编码的数据
        """
        encoded_data = data.encode('utf-8')
        length = len(encoded_data)
        self.__socket.sendall(struct.pack('>H', length))  # 先发送两个字节表示字符串长度（大端序）
        self.__socket.sendall(encoded_data)  # 再发送实际的字符串字节数据

    def _recv_utf8_data(self):
        """
        按照类似Java readUTF的格式接收UTF-8编码的数据
        """
        length_data = self.__socket.recv(2)  # 先接收两个字节获取字符串长度
        length = struct.unpack('>H', length_data)[0]  # 解包获取长度值（大端序）
        data = b''
        while len(data) < length:
            chunk = self.__socket.recv(length - len(data))
            if not chunk:
                break
            data += chunk
        return data.decode('utf-8')

    def __heartbeat_check(self):
        while self.__running:
            if self.__socket is None or not self.__is_connected():
                print_info("尝试建立连接...")
                self.__connect()
            time.sleep(3)  # 心跳检测间隔

    def __connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect(('localhost', 18000))
            TraceSocket.device_socket_dict[self.__device.serial] = self
            print_success("建立新连接: " + str(self.__socket))
        except Exception as e:
            print_error("连接异常! - " + str(e))

    def __is_connected(self):
        if self.__socket is not None:
            try:
                self.__socket.settimeout(0.01)
                self.__socket.getpeername()
                return True
            except socket.timeout:
                return False
            except Exception:
                return False
        return False

    def __close_socket(self):
        if self.__socket is not None:
            try:
                self.__socket.close()
                print_success("连接已成功关闭")
            except Exception as e:
                print_error("关闭socket异常: " + str(e))
            finally:
                self.__socket = None

    def __generate_cookie(self):
        if self.__trace_cookie is not None:
            print_warning(f"{self.__recent_operation_name}没有结束，兜底执行结束，请检查代码逻辑")
            self.stop_trace()
        cookie = datetime.datetime.now().strftime("%H%M%S")
        self.__trace_cookie = cookie

    def start_trace(self, operation_name:str):
        """
        开始记录trace，传入一个操作名作为trace的名字
        请及时结束记录trace，当前需要手动调用 stop_trace 结束抓取
        如果未结束抓取，而重复执行start
        会有兜底逻辑，在第二个start开始的时候结束上一个start
        :param operation_name: 操作名称
        :return: 无
        """
        operation_name = operation_name.replace("_", "-")
        self.__generate_cookie()
        self.__recent_operation_name = operation_name
        self.__send_message(f"start_{operation_name}_{self.__trace_cookie}")

    def stop_trace(self):
        """
        结束记录trace
        :return:
        """
        self.__send_message(f"end_{self.__recent_operation_name}_{self.__trace_cookie}")
        self.__trace_cookie = None

    def __send_message(self, message:str, need_retry=True):
        if self.__socket is not None and self.__is_connected():
            try:
                print_info("准备发送数据: " + message)
                self._send_utf8_data(message)
                print_info("发送数据完成: " + message)
            except Exception as e:
                print_warning("发送消息异常: " + str(e))
                if need_retry:
                    print_info("重新连接并发送消息: " + message)
                    self.__connect()
                    self.__send_message(message, need_retry=False)
        else:
            if need_retry:
                print_info("重新连接并发送消息: " + message)
                self.__connect()
                self.__send_message(message, need_retry=False)
            else:
                print_warning("未连接到服务器，重新连接")

    def stop_socket(self):
        """
        关闭socket
        :return:
        """
        self.__stop_performance_test_helper_process()
        self.__running = False
        self.__close_socket()
        self.__heartbeat_thread.join()


if __name__ == "__main__":
    socket_test = TraceSocket()
    try:
        # 这里可以调用send_message方法发送消息
        # socket_test.send_message("自定义消息")
        while True:
            data = input("请输出你想发送的内容：")
            socket_test.__send_message(data)
            time.sleep(1)
    except KeyboardInterrupt:
        socket_test.stop_socket()
