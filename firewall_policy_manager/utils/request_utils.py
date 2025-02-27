#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
신청 정보 관련 유틸리티 기능을 제공하는 모듈
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)

class RequestUtils:
    """신청 정보 관련 유틸리티 기능을 제공하는 클래스"""
    
    @staticmethod
    def find_auto_extension_id(info_df):
        """
        자동 연장 ID를 찾습니다.
        
        Args:
            info_df (DataFrame): 정보 DataFrame
            
        Returns:
            Series: 자동 연장 ID 시리즈
        """
        # REQUEST_STATUS가 문자열인 경우 숫자로 변환
        try:
            # 숫자로 변환 가능한 경우
            status_col = pd.to_numeric(info_df['REQUEST_STATUS'], errors='coerce')
            filtered_df = info_df[status_col.isin([98, 99])]['REQUEST_ID'].drop_duplicates()
        except:
            # 문자열인 경우
            filtered_df = info_df[info_df['REQUEST_STATUS'].isin(['98', '99'])]['REQUEST_ID'].drop_duplicates()
        
        logger.info(f"자동 연장 ID {len(filtered_df)}개를 찾았습니다.")
        return filtered_df 