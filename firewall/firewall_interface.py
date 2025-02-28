# firewall/firewall_interface.py
from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional

class FirewallInterface(ABC):
    @abstractmethod
    def get_system_info(self) -> pd.DataFrame:
        """시스템 정보를 DataFrame으로 반환합니다."""
        pass

    @abstractmethod
    def export_security_rules(self) -> pd.DataFrame:
        """보안 규칙 데이터를 DataFrame으로 반환합니다."""
        pass

    @abstractmethod
    def export_network_objects(self) -> pd.DataFrame:
        """네트워크 객체 정보를 DataFrame으로 반환합니다.
        Returns:
            pd.DataFrame: Name, Type, Value 컬럼을 가진 DataFrame
        """
        pass

    @abstractmethod
    def export_network_group_objects(self) -> pd.DataFrame:
        """네트워크 그룹 객체 정보를 DataFrame으로 반환합니다.
        Returns:
            pd.DataFrame: Group Name, Entry 컬럼을 가진 DataFrame
        """
        pass

    @abstractmethod
    def export_service_objects(self) -> pd.DataFrame:
        """서비스 객체 정보를 DataFrame으로 반환합니다.
        Returns:
            pd.DataFrame: Name, Protocol, Port 컬럼을 가진 DataFrame
        """
        pass

    @abstractmethod
    def export_service_group_objects(self) -> pd.DataFrame:
        """서비스 그룹 객체 정보를 DataFrame으로 반환합니다.
        Returns:
            pd.DataFrame: Group Name, Entry 컬럼을 가진 DataFrame
        """
        pass

    @abstractmethod
    def export_usage_logs(self, days: Optional[int] = None) -> pd.DataFrame:
        """정책 사용이력을 DataFrame으로 반환합니다.
        Args:
            days: 조회할 기간 (일), None인 경우 전체 기간
        Returns:
            pd.DataFrame: Rule Name, Last Hit Date, Unused Days 컬럼을 가진 DataFrame
        """
        pass