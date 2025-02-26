#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
설정 파일을 관리하는 모듈
"""

import json
import logging
import sys

logger = logging.getLogger(__name__)

class ConfigManager:
    """설정 파일을 관리하는 클래스"""
    
    def __init__(self, config_file='config.json'):
        """
        설정 파일을 로드합니다.
        
        Args:
            config_file (str): 설정 파일 경로
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            logger.info(f"설정 파일 '{config_file}'을 성공적으로 로드했습니다.")
        except FileNotFoundError:
            logger.error(f"설정 파일 '{config_file}'을 찾을 수 없습니다.")
            sys.exit(1)
        except json.JSONDecodeError:
            logger.error(f"설정 파일 '{config_file}'의 형식이 올바르지 않습니다.")
            sys.exit(1)
    
    def get(self, key, default=None):
        """
        설정값을 가져옵니다.
        
        Args:
            key (str): 설정 키 (점으로 구분된 경로)
            default: 기본값
            
        Returns:
            설정값 또는 기본값
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            logger.warning(f"설정 키 '{key}'를 찾을 수 없습니다. 기본값 '{default}'를 사용합니다.")
            return default 