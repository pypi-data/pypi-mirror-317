from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any, Dict
import re
import json

class NetworkType(Enum):
    YD_WIRELESS = "@yd"      # 移动无线
    YD_WIRED = "@ydyx"       # 移动有线
    STUDENT = "@stu"         # 学生
    TEACHER = "@tch"         # 教师
    TELECOM = "@dxwx"        # 电信

class Account:
    def __init__(self, student_id: str, network_type: NetworkType, password: str):
        self.student_id = student_id
        self.network_type = network_type
        self.password = password

    @property
    def username(self) -> str:
        """获取完整用户名"""
        return f"{self.student_id}{self.network_type.value}"

class AccountFactory:
    @staticmethod
    def create_account(student_id: str, network_type: NetworkType, password: str) -> Account:
        # 验证学号格式
        if not student_id.isdigit():
            raise ValueError("Student ID must contain only digits")

        # 验证学号长度
        if len(student_id) != 12:
            raise ValueError("Student ID must be 12 digits")

        # 验证密码不为空
        if not password:
            raise ValueError("Password cannot be empty")

        return Account(student_id, network_type, password)

@dataclass
class NetworkConfig:
    """Network configuration constants"""
    INIT_URL: str = "http://172.16.245.50"
    GET_CHALLENGE_API: str = f"{INIT_URL}/cgi-bin/get_challenge"
    SRUN_PORTAL_API: str = f"{INIT_URL}/cgi-bin/srun_portal"
    GET_INFO_API: str = f"{INIT_URL}/cgi-bin/rad_user_info"
    N: str = '200'
    TYPE: str = '1'
    AC_ID: str = '2'
    ENC: str = "srun_bx1"

@dataclass
class BaseResponse:
    """基础响应类"""
    raw_response: str
    parsed_data: Dict[str, Any]

class ResponseParser:
    """响应解析器"""
    @staticmethod
    def parse_callback_response(response_text: str) -> Dict[str, Any]:
        """解析jQuery回调格式的响应
        
        Args:
            response_text: jQuery112404953031673771599_1709723579123({"error":"ok",...})
            
        Returns:
            解析后的字典对象
        """
        # 提取回调函数中的JSON字符串
        match = re.search(r'jQuery\d+_\d+\((.*)\)', response_text)
        if not match:
            raise ValueError("Invalid response format: not a jQuery callback")
            
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in response: {e}")

@dataclass
class SrunResponse(BaseResponse):
    """深澜响应基类"""
    success: bool
    message: str
    error_code: Optional[str] = None

    @classmethod
    def from_response(cls, response_text: str) -> 'SrunResponse':
        """从响应文本创建响应对象"""
        parsed_data = ResponseParser.parse_callback_response(response_text)
        
        return cls(
            raw_response=response_text,
            parsed_data=parsed_data,
            success=parsed_data.get('error') == 'ok',
            message=parsed_data.get('error_msg', ''),
            error_code=parsed_data.get('ecode')
        )

@dataclass
class LoginResponse(SrunResponse):
    """登录响应"""
    policy_message: Optional[str] = None

    @classmethod
    def from_response(cls, response_text: str) -> 'LoginResponse':
        """从响应文本创建登录响应对象"""
        parsed_data = ResponseParser.parse_callback_response(response_text)
        
        # 检查是否已经在线
        if parsed_data.get('suc_msg') == 'ip_already_online_error':
            return cls(
                raw_response=response_text,
                parsed_data=parsed_data,
                success=False,
                message="IP already online",
                policy_message=None
            )
            
        # 检查消息
        policy_message = None
        ploy_msg = parsed_data.get('ploy_msg', '')
        if ploy_msg and not ploy_msg.startswith('E0000'):
            policy_message = ploy_msg
            
        return cls(
            raw_response=response_text,
            parsed_data=parsed_data,
            success=parsed_data.get('error') == 'ok',
            message=parsed_data.get('error_msg', 'Login successful' if parsed_data.get('error') == 'ok' else 'Login failed'),
            error_code=parsed_data.get('ecode'),
            policy_message=policy_message
        )

@dataclass
class LogoutResponse(SrunResponse):
    """注销响应"""
    
    @classmethod
    def from_response(cls, response_text: str) -> 'LogoutResponse':
        """从响应文本创建注销响应对象"""
        parsed_data = ResponseParser.parse_callback_response(response_text)
        
        return cls(
            raw_response=response_text,
            parsed_data=parsed_data,
            success=parsed_data.get('error') == 'ok',
            message=parsed_data.get('error_msg', 'Logout successful' if parsed_data.get('error') == 'ok' else 'Logout failed'),
            error_code=parsed_data.get('ecode')
        )

@dataclass
class StatusResponse(SrunResponse):
    """状态响应"""
    is_online: bool = False
    username: Optional[str] = None
    used_bytes: Optional[int] = None
    used_seconds: Optional[int] = None
    balance: Optional[float] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    domain: Optional[str] = None
    checkout_date: Optional[str] = None
    
    @classmethod
    def from_response(cls, response_text: str) -> 'StatusResponse':
        """从响应文本创建状态响应对象"""
        parsed_data = ResponseParser.parse_callback_response(response_text)
        
        is_ok = parsed_data.get('error') == 'ok'
        return cls(
            raw_response=response_text,
            parsed_data=parsed_data,
            success=is_ok,
            is_online=is_ok,
            message='User is online' if is_ok else parsed_data.get('error_msg', 'User is offline'),
            error_code=parsed_data.get('ecode'),
            username=parsed_data.get('user_name'),
            used_bytes=int(parsed_data.get('sum_bytes', 0)),
            used_seconds=int(parsed_data.get('sum_seconds', 0)),
            balance=float(parsed_data.get('user_balance', 0)),
            ip_address=parsed_data.get('online_ip'),
            mac_address=parsed_data.get('user_mac'),
            domain=parsed_data.get('domain'),
            checkout_date=parsed_data.get('checkout_date')
        )

    def format_used_traffic(self) -> str:
        """格式化流量使用量"""
        if self.used_bytes is None:
            return "未知"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(self.used_bytes)
        unit_index = 0
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
            
        return f"{size:.2f} {units[unit_index]}"

    def format_used_time(self) -> str:
        """格式化使用时长"""
        if self.used_seconds is None:
            return "未知"
            
        hours = self.used_seconds // 3600
        minutes = (self.used_seconds % 3600) // 60
        seconds = self.used_seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"