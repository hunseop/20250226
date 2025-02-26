#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
방화벽 정책 관리 프로세스 실행 스크립트
"""

import os
import sys

# 패키지 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firewall_policy_manager.main import main

if __name__ == "__main__":
    main() 