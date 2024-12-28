import wmi
import pythoncom
import time
from typing import Callable, Dict, Any, Optional
import winreg
import re
from datetime import datetime

class USBEventMonitor:
    """USB设备事件监控器"""
    
    # 类常量定义
    SEPARATOR = '=' * 60
    LOCATION_FIELDS = {"实际设备ID", "设备位置"}
    DEVICE_ATTRIBUTES = [
        'Caption', 'ClassGuid', 'ConfigManagerErrorCode', 
        'ConfigManagerUserConfig', 'CreationClassName', 'Description',
        'Manufacturer', 'Name', 'PNPClass', 'PNPDeviceID',
        'Present', 'Service', 'Status', 'SystemCreationClassName', 
        'SystemName'
    ]
    LIST_ATTRIBUTES = ['CompatibleID', 'HardwareID']
    
    def __init__(self, 
                 on_connect: Optional[Callable[[Dict[str, Any]], None]] = None,
                 on_disconnect: Optional[Callable[[Dict[str, Any]], None]] = None,
                 check_interval: float = 0.2,
                 enable_print: bool = False,
                 enable_location: bool = True):
        """
        初始化USB监控器
        :param on_connect: USB设备连接时的回调函数
        :param on_disconnect: USB设备断开时的回调函数
        :param check_interval: 检查间隔时间(秒)
        :param enable_print: 是否打印设备信息
        :param enable_location: 是否启用设备位置查询
        """
        self._on_connect = on_connect
        self._on_disconnect = on_disconnect
        self._is_running = False
        self._check_interval = max(0.1, check_interval)  # 确保最小间隔
        self._enable_print = enable_print
        self._enable_location = enable_location
        self._device_info_cache = {}
        # 根据是否启用位置查询设置基本字段
        self._basic_fields = {"设备ID"}.union(self.LOCATION_FIELDS if enable_location else set())

    def _get_device_info(self, device_id: str, device_obj: Any = None) -> Dict[str, Any]:
        """获取USB设备信息"""
        # 只有在没有新设备对象时才使用缓存
        if device_obj is None and device_id in self._device_info_cache:
            return self._device_info_cache[device_id].copy()
            
        if not device_id:
            return {"设备ID": "未知设备"}
            
        # 基本信息
        info = {"设备ID": device_id}
        
        # 如果启用位置查询，获取实际设备ID和位置
        if self._enable_location:
            real_id, location = self._get_usb_location(device_id)
            if real_id:
                info["实际设备ID"] = real_id
            if location:
                info["设备位置"] = location

        # 添加设备对象的属性
        if device_obj is not None:
            # 处理列表类型的属性
            for list_attr in self.LIST_ATTRIBUTES:
                if hasattr(device_obj, list_attr):
                    attr_value = getattr(device_obj, list_attr)
                    if attr_value:
                        info[list_attr] = ', '.join(attr_value)
            
            # 处理其他属性
            for attr in self.DEVICE_ATTRIBUTES:
                if value := getattr(device_obj, attr, ''):
                    info[attr] = value
            
            # 缓存设备信息
            self._device_info_cache[device_id] = info.copy()
                
        return info

    def _get_usb_location(self, device_path: str) -> tuple[str, str]:
        """获取USB设备ID和位置信息"""
        try:
            # 快速检查路径格式是否有效
            if not device_path or device_path.count('&') != 1:
                return '', ''
                
            parts = device_path.split("\\")
            device_id = parts[-1]
            
            # 构造注册表路径
            reg_path = "SYSTEM\\CurrentControlSet\\Enum\\" + "\\".join(parts[:-1])
            
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ) as key:
                # 获取实际设备ID
                real_id = device_id if device_id.isdigit() else winreg.EnumKey(key, 0)
                
                # 获取位置信息
                with winreg.OpenKey(key, real_id) as dev_key:
                    loc = winreg.QueryValueEx(dev_key, 'LocationInformation')[0]
                    # 使用更快的字符串处理方法
                    first_hash = loc.find('#') + 1
                    first_dot = loc.find('.')
                    last_hash = loc.rfind('#') + 1
                    
                    hub = int(loc[first_hash:first_dot])
                    port = int(loc[last_hash:])
                    return real_id, f"{port}-{hub}"
                    
        except (WindowsError, ValueError, IndexError):
            return '', ''

    def _notify_event(self, info: Dict[str, Any], event_type: str) -> None:
        """通知事件（打印信息和调用回调）"""
        if self._enable_print:
            # 预先构建输出信息
            output_lines = [
                self.SEPARATOR,
                f"USB设备{event_type}",
                self.SEPARATOR
            ]
            
            # 添加基本信息
            for key in self._basic_fields:
                if value := info.get(key):
                    output_lines.append(f"{key:15}: {value}")
            
            # 添加其他信息
            other_info = sorted((k, v) for k, v in info.items() 
                              if k not in self._basic_fields and v)
            if other_info:
                for key, value in other_info:
                    output_lines.append(f"{key:15}: {value}")
                    
            output_lines.append(self.SEPARATOR)
            
            # 一次性打印所有信息
            print('\n'.join(output_lines))

        # 调用回调函数
        callback = self._on_connect if event_type == "连接" else self._on_disconnect
        if callback is not None:
            try:
                callback(info)
            except Exception as e:
                if self._enable_print:
                    print(f"回调函数执行出错: {e}")

    def _get_current_time(self) -> str:
        """获取当前时间的格式化字符串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _handle_connect(self, device_id: str, device_obj: Any = None) -> None:
        """处理设备连接事件"""
        try:
            # 确保设备ID格式正确
            device_id = device_id.replace('\\\\', '\\')
            info = self._get_device_info(device_id, device_obj)
            info["状态"] = "已连接"
            info["添加时间"] = self._get_current_time()
            self._notify_event(info, "连接")
        except Exception as e:
            if self._enable_print:
                print(f"处理设备事件时出错: {e}")

    def _extract_device_id(self, usb_info: str) -> str:
        """从USB信息字符串中提取设备ID"""
        try:
            # 使用预编译的正则表达式
            if not hasattr(self, '_device_id_pattern'):
                self._device_id_pattern = re.compile(r'Dependent.*?DeviceID=\\"([^"]+)\\"')
                
            if match := self._device_id_pattern.search(usb_info):
                device_id = match.group(1)
                # 确保设备ID格式正确
                return device_id.replace('\\\\', '\\')
            return ""
        except Exception:
            return ""

    def _handle_disconnect(self, usb_info: str) -> None:
        """处理设备断开事件"""
        try:
            device_id = self._extract_device_id(usb_info)
            # 确保设备ID格式正确
            device_id = device_id.replace('\\\\', '\\')
            if device_id in self._device_info_cache:
                info = self._device_info_cache[device_id].copy()
                info["状态"] = "已断开"
                info["断开时间"] = self._get_current_time()
                self._notify_event(info, "断开")
                self._device_info_cache.pop(device_id, None)
            else:
                info = {
                    "设备ID": device_id,
                    "状态": "已断开",
                    "断开时间": self._get_current_time()
                }
                self._notify_event(info, "断开")
        except Exception as e:
            if self._enable_print:
                print(f"处理设备事件时出错: {e}")

    def start(self) -> None:
        """启动监控"""
        if self._is_running:
            return
            
        if self._enable_print:
            print("USB监控已启动...\n按Ctrl+C停止监控...")
            
        self._is_running = True
        
        try:
            pythoncom.CoInitialize()
            wmi_obj = wmi.WMI()
            watcher = wmi_obj.watch_for(
                raw_wql=f"SELECT * FROM __InstanceOperationEvent WITHIN {self._check_interval} "
                       "WHERE TargetInstance ISA 'Win32_USBControllerDevice'"
            )
            
            while self._is_running:
                try:
                    usb = watcher()
                    if not usb:
                        continue
                    
                    if usb.event_type == 'creation' and hasattr(usb, 'Dependent'):
                        device_id = usb.Dependent.DeviceID
                        self._handle_connect(device_id, usb.Dependent)
                    elif usb.event_type == 'deletion':
                        self._handle_disconnect(str(usb))
                        
                except Exception as e:
                    if self._enable_print:
                        print(f"监控过程出错: {e}")
                    time.sleep(0.1)
        except Exception as e:
            if self._enable_print:
                print(f"监控过程出错: {e}")
        finally:
            self.stop()

    def stop(self) -> None:
        """停止监控"""
        if not self._is_running:
            return
            
        self._is_running = False
        self._device_info_cache.clear()  # 清除缓存
        
        if self._enable_print:
            print("\nUSB监控已停止")

def main():
    """演示使用方法"""
    def on_connect(info: Dict[str, Any]) -> None:
        """设备连接回调示例"""
        device_id = info.get('设备ID', '未知设备')
        print(f"自定义处理 - 设备已连接: {device_id}")
        
    def on_disconnect(info: Dict[str, Any]) -> None:
        """设备断开回调示例"""
        device_id = info.get('设备ID', '未知设备')
        print(f"自定义处理 - 设备已断开: {device_id}")
    
    # 创建监控器（启用打印功能）
    monitor = USBEventMonitor(
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        check_interval=0.4,  # 使用0.4秒的检查间隔
        enable_print=True,  # 演示时启用打印
        enable_location=True  # 启用设备位置查询
    )
    monitor.start()

if __name__ == "__main__":
    main() 