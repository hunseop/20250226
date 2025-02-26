#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
방화벽 정책 관리 프로세스 메인 스크립트
"""

import logging
import sys
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('firewall_policy_manager.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 패키지 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from firewall_policy_manager.core.config_manager import ConfigManager
from firewall_policy_manager.utils.file_manager import FileManager
from firewall_policy_manager.utils.excel_manager import ExcelManager
from firewall_policy_manager.processors.request_parser import RequestParser
from firewall_policy_manager.processors.request_extractor import RequestExtractor
from firewall_policy_manager.processors.request_info_adder import RequestInfoAdder
from firewall_policy_manager.processors.mis_id_adder import MisIdAdder
from firewall_policy_manager.processors.exception_handler import ExceptionHandler
from firewall_policy_manager.processors.duplicate_policy_classifier import DuplicatePolicyClassifier
from firewall_policy_manager.processors.policy_usage_processor import PolicyUsageProcessor
from firewall_policy_manager.processors.notification_classifier import NotificationClassifier

def select_task():
    """
    작업을 선택합니다.
    
    Returns:
        int: 선택된 작업 번호
    """
    print("\n방화벽 정책 관리 프로세스")
    print("=" * 50)
    print("시작할 작업 번호를 입력해주세요.")
    print("1. Description에서 신청번호 파싱하기")
    print("2. 정책파일에서 신청번호 추출하기")
    print("3. 정책파일에 MIS ID 추가하기")
    print("4. 정책파일에 신청정보 추가하기")
    print("5. 팔로알토 정책에서 예외처리하기")
    print("6. 시큐아이 정책에서 예외처리하기")
    print("7. 중복정책 공지/삭제 분류하기")
    print("8. 중복정책 분류 결과를 정책 파일에 추가하기")
    print("9. 미사용 정책 정보를 정책 파일에 추가하기")
    print("10. 정리대상 별 공지파일 분류하기")
    print("0. 종료")
    print("=" * 50)

    while True:
        try:
            choice = input("작업 번호 (1-10, 종료: 0): ")
            if choice.isdigit():
                choice = int(choice)
                if 0 <= choice <= 10:
                    return choice
            print('유효하지 않은 번호입니다. 다시 시도하세요.')
        except ValueError:
            print("유효하지 않은 입력입니다. 다시 시도하세요.")

def main():
    """
    메인 함수
    """
    try:
        # 설정 관리자 초기화
        config_manager = ConfigManager()
        
        # 파일 관리자 초기화
        file_manager = FileManager(config_manager)
        
        # Excel 관리자 초기화
        excel_manager = ExcelManager(config_manager)
        
        # 작업 선택
        task = select_task()
        
        if task == 0:
            print("프로그램을 종료합니다.")
            sys.exit(0)
        
        # 선택된 작업 실행
        if task == 1:
            # Description에서 신청번호 파싱하기
            request_parser = RequestParser(config_manager)
            result = request_parser.parse_request_type(file_manager)
        elif task == 2:
            # 정책파일에서 신청번호 추출하기
            request_extractor = RequestExtractor(config_manager)
            result = request_extractor.extract_request_id(file_manager)
        elif task == 3:
            # 정책파일에 MIS ID 추가하기
            mis_id_adder = MisIdAdder(config_manager)
            result = mis_id_adder.add_mis_id(file_manager)
        elif task == 4:
            # 정책파일에 신청정보 추가하기
            request_info_adder = RequestInfoAdder(config_manager)
            result = request_info_adder.add_request_info(file_manager)
        elif task == 5:
            # 팔로알토 정책에서 예외처리하기
            exception_handler = ExceptionHandler(config_manager)
            result = exception_handler.paloalto_exception(file_manager)
        elif task == 6:
            # 시큐아이 정책에서 예외처리하기
            exception_handler = ExceptionHandler(config_manager)
            result = exception_handler.secui_exception(file_manager)
        elif task == 7:
            # 중복정책 공지/삭제 분류하기
            duplicate_policy_classifier = DuplicatePolicyClassifier(config_manager)
            result = duplicate_policy_classifier.organize_redundant_file(file_manager)
        elif task == 8:
            # 중복정책 분류 결과를 정책 파일에 추가하기
            duplicate_policy_classifier = DuplicatePolicyClassifier(config_manager)
            result = duplicate_policy_classifier.add_duplicate_status(file_manager)
        elif task == 9:
            # 미사용 정책 정보를 정책 파일에 추가하기
            policy_usage_processor = PolicyUsageProcessor(config_manager)
            result = policy_usage_processor.add_usage_status(file_manager)
        elif task == 10:
            # 정리대상 별 공지파일 분류하기
            notification_classifier = NotificationClassifier(config_manager)
            result = notification_classifier.classify_notifications(file_manager, excel_manager)
        
        if result:
            print("작업이 성공적으로 완료되었습니다.")
        else:
            print("작업이 실패했습니다.")
        
    except Exception as e:
        logger.exception(f"프로그램 실행 중 오류 발생: {e}")
        print(f"오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 