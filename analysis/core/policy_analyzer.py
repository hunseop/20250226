"""
방화벽 정책 분석을 위한 메인 클래스입니다.
"""

import pandas as pd
import logging
from typing import Optional, Dict, List
from datetime import datetime

from .redundancy_analyzer import RedundancyAnalyzer
from .change_analyzer import ChangeAnalyzer
from ..utils.excel_handler import ExcelHandler

class PolicyAnalyzer:
    """방화벽 정책 분석을 위한 통합 클래스"""
    
    def __init__(self):
        """PolicyAnalyzer 초기화"""
        self.logger = logging.getLogger(__name__)
        self.redundancy_analyzer = RedundancyAnalyzer()
        self.change_analyzer = ChangeAnalyzer()
        self.excel_handler = ExcelHandler()
    
    def analyze_redundancy(self, 
                          df: pd.DataFrame, 
                          vendor: str, 
                          output_file: str,
                          **kwargs) -> pd.DataFrame:
        """
        중복 정책 분석을 수행합니다.
        
        Args:
            df: 분석할 정책 데이터프레임
            vendor: 방화벽 벤더 (예: 'paloalto', 'ngf')
            output_file: 결과를 저장할 파일 경로
            **kwargs: 추가 매개변수
        
        Returns:
            분석 결과 데이터프레임
        """
        try:
            self.logger.info(f"{vendor} 방화벽 정책 중복 분석 시작")
            result_df = self.redundancy_analyzer.analyze(df, vendor, **kwargs)
            self.excel_handler.save_redundancy_analysis(result_df, output_file)
            self.logger.info(f"중복 분석 결과가 {output_file}에 저장되었습니다.")
            return result_df
        except Exception as e:
            self.logger.error(f"중복 정책 분석 중 오류 발생: {e}")
            raise
    
    def analyze_changes(self,
                       df_before: pd.DataFrame,
                       df_after: pd.DataFrame,
                       output_file: str,
                       **kwargs) -> Dict[str, pd.DataFrame]:
        """
        정책 변경사항을 분석합니다.
        
        Args:
            df_before: 이전 정책 데이터프레임
            df_after: 현재 정책 데이터프레임
            output_file: 결과를 저장할 파일 경로
            **kwargs: 추가 매개변수
        
        Returns:
            변경사항 분석 결과를 담은 딕셔너리
        """
        try:
            self.logger.info("정책 변경사항 분석 시작")
            results = self.change_analyzer.analyze(df_before, df_after, **kwargs)
            self.excel_handler.save_change_analysis(results, output_file)
            self.logger.info(f"변경사항 분석 결과가 {output_file}에 저장되었습니다.")
            return results
        except Exception as e:
            self.logger.error(f"변경사항 분석 중 오류 발생: {e}")
            raise
    
    def analyze_usage(self,
                     df: pd.DataFrame,
                     usage_data: pd.DataFrame,
                     output_file: str,
                     **kwargs) -> pd.DataFrame:
        """
        정책 사용현황을 분석합니다.
        
        Args:
            df: 분석할 정책 데이터프레임
            usage_data: 정책 사용 데이터
            output_file: 결과를 저장할 파일 경로
            **kwargs: 추가 매개변수
        
        Returns:
            사용현황 분석 결과 데이터프레임
        """
        try:
            self.logger.info("정책 사용현황 분석 시작")
            # TODO: 사용현황 분석 로직 구현
            pass
        except Exception as e:
            self.logger.error(f"사용현황 분석 중 오류 발생: {e}")
            raise 