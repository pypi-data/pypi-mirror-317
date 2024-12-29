import re
import time
import requests
from typing import Dict, Optional
import hmac
import hashlib
import json
from .logger import get_logger
from .models import Account, NetworkConfig, LoginResponse, LogoutResponse, StatusResponse
from .encryption import Encryptor
from .exceptions import NetworkError, AuthenticationError

class LoginSession:
    """Main login session handler"""
    def __init__(self, account: Optional[Account] = None):
        self.logger = get_logger(__name__)
        self.account = account
        self.config = NetworkConfig()
        self.token = None
        self.ip = None
        self.info = None
        self.hmd5 = None
        self.chksum = None
        self.headers = self._get_headers()
        self.cookies = self._get_cookies() if account else {"lang": "zh-CN"}

    def _get_headers(self) -> Dict:
        """Generate request headers"""
        return {
            "Host": "172.16.245.50",
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; M2012K11G Build/AP2A.240905.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.81 Mobile Safari/537.36',
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def _get_cookies(self) -> Dict:
        """Generate request cookies based on network type"""
        return {
            "lang": "zh-CN",
            "domain": self.account.network_type.value if self.account else "",
        }

    def _init_getip(self):
        """Initialize and get IP address"""
        try:
            init_res = requests.get(self.config.INIT_URL, headers=self.headers)
            init_res.raise_for_status()
            ip_match = re.search('id="user_ip" value="(.*?)"', init_res.text)
            if not ip_match:
                raise NetworkError("Failed to extract IP address")
            self.ip = ip_match.group(1)
            self.logger.debug(f"IP initialized: {self.ip}")
        except requests.RequestException as e:
            raise NetworkError(f"Failed to initialize IP: {str(e)}")

    def _update_referer(self):
        """Update referer in headers"""
        self.headers['Referer'] = (
            f'{self.config.INIT_URL}/srun_portal_phone?ac_id={self.config.AC_ID}'
            f'&ip-address=http://172.16.245.50/srun_portal_phone?ac_id=2'
            f'&ip-address=http%3A%2F%2Fconnect.rom.miui.com%2Fgenerate_204'
            f'&theme=basic&wlanuserip={self.ip}'
        )

    def _remove_referer(self):
        """Remove referer in headers"""
        if 'Referer' in self.headers:
            del self.headers['Referer']

    def _get_token(self):
        """Get authentication token"""
        try:
            params = {
                "callback": f"jQuery112404953031673771599_{int(time.time() * 1000)}",
                "username": self.account.username,
                "ip": self.ip,
                "_": int(time.time() * 1000),
            }
            self._update_referer()
            token_res = requests.get(self.config.GET_CHALLENGE_API, params=params, headers=self.headers)
            token_res.raise_for_status()
            self._remove_referer()
            
            token_match = re.search('"challenge":"(.*?)"', token_res.text)
            if not token_match:
                raise AuthenticationError("Failed to extract token")
            self.token = token_match.group(1)
            self.logger.debug(f"Token received: {self.token}")
        except requests.RequestException as e:
            raise NetworkError(f"Failed to get token: {str(e)}")

    def _prepare_login_data(self):
        """Prepare login data"""
        info = f"{{\"username\":\"{self.account.username}\",\"password\":\"{self.account.password}\",\"ip\":\"{self.ip}\",\"acid\":\"{self.config.AC_ID}\",\"enc_ver\":\"{self.config.ENC}\"}}"
        self.info = f"{'{SRBX1}'}{Encryptor.get_base64(Encryptor.get_xencode(info, self.token))}"
        self.hmd5 = hmac.new(self.token.encode(), self.account.password.encode(), hashlib.md5).hexdigest()
        self.chksum = hashlib.sha1(
            "".join([
                self.token, self.account.username, 
                self.token, self.hmd5,
                self.token, self.config.AC_ID, 
                self.token, self.ip,
                self.token, self.config.N, 
                self.token, self.config.TYPE,
                self.token, self.info
            ]).encode()
        ).hexdigest()
        self.logger.debug("Login data prepared.")

    
    def get_status(self) -> StatusResponse:
        """Get login status"""
        try:
            params = {
                "callback": f"jQuery112404953031673771599_{int(time.time() * 1000)}",
                "_": int(time.time() * 1000),
            }
            response = requests.get(
                self.config.GET_INFO_API, 
                headers=self.headers, 
                params=params, 
                cookies=self.cookies
            )
            response.raise_for_status()
            
            return StatusResponse.from_response(response.text)
        except requests.RequestException as e:
            raise NetworkError(f"Failed to get status: {str(e)}")

    def login(self) -> LoginResponse:
        """Perform login"""
        try:
            self._init_getip()
            self._get_token()
            self._prepare_login_data()

            params = {
                "callback": f"jQuery112404953031673771599_{int(time.time() * 1000)}",
                "action": "login",
                "username": self.account.username,
                "password": "{MD5}" + self.hmd5,
                "os": "AndroidOS",
                "name": "Smartphones/PDAs/Tablets",
                "double_stack": "0",
                "chksum": self.chksum,
                "info": self.info,
                "n": self.config.N,
                "type": self.config.TYPE,
                "ac_id": self.config.AC_ID,
                "ip": self.ip,
                "_": int(time.time() * 1000),
            }
            self._update_referer()
            response = requests.get(
                self.config.SRUN_PORTAL_API, 
                headers=self.headers, 
                params=params, 
                cookies=self.cookies
            )
            response.raise_for_status()
            self._remove_referer()
            
            return LoginResponse.from_response(response.text)
        except requests.RequestException as e:
            raise NetworkError(f"Failed to login: {str(e)}")

    def logout(self) -> LogoutResponse:
        """Perform logout"""
        try:
            params = {
                "callback": f"jQuery112404953031673771599_{int(time.time() * 1000)}",
                "action": "logout",
                "username": self.account.username,
                "ac_id": self.config.AC_ID,
                "ip": self.ip,
                "_": int(time.time() * 1000),
            }
            self._update_referer()
            response = requests.get(
                self.config.SRUN_PORTAL_API, 
                headers=self.headers, 
                params=params, 
                cookies=self.cookies
            )
            response.raise_for_status()
            self._remove_referer()
            
            return LogoutResponse.from_response(response.text)
        except requests.RequestException as e:
            raise NetworkError(f"Failed to logout: {str(e)}")