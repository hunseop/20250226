# 방화벽 정책 관리 프로세스

방화벽 정책 관리 프로세스를 자동화하는 도구입니다. 이 도구는 방화벽 정책 파일을 처리하고, 신청 정보를 추출하며, 다양한 기준으로 정책을 분류하는 기능을 제공합니다.

## 기능

1. **신청번호 파싱**: Description 필드에서 신청번호 등 정보 추출
2. **신청번호 추출**: 신청번호(Request ID)만 추출하여 타부서 전달
3. **MIS ID 추가**: 정책에 누락된 MIS ID 정보 추가
4. **신청정보 추가**: 신청번호 기반으로 타부서 제공 정보 매핑
5. **예외처리**: 방화벽 종류에 따라 예외처리 수행
   - 팔로알토
   - 시큐아이
6. **중복정책 분류**: 중복정책을 공지용/삭제용으로 분류
7. **중복정책 상태 추가**: 중복정책 분류 결과를 정책 파일에 추가
8. **미사용 정책 정보 추가**: 미사용 정책 정보를 정책 파일에 추가
9. **정리대상 분류**: 최종 정책 파일을 여러 기준으로 분류하여 공지용 파일 생성

## 설치 및 실행

### 요구사항

- Python 3.6 이상
- 필요한 패키지: pandas, openpyxl

### 패키지 설치

```bash
pip install pandas openpyxl
```

### 설정 파일

프로그램을 실행하기 전에 `config.json` 파일을 확인하고 필요에 따라 수정하세요. 이 파일에는 컬럼 정보, 패턴, 파일 명명 규칙 등의 설정이 포함되어 있습니다.

### 실행 방법

```bash
python run_firewall_policy_manager.py
```

또는 실행 권한이 있는 경우:

```bash
./run_firewall_policy_manager.py
```

## 프로젝트 구조

```
firewall_policy_manager/
├── core/
│   ├── __init__.py
│   └── config_manager.py
├── utils/
│   ├── __init__.py
│   ├── file_manager.py
│   └── excel_manager.py
├── processors/
│   ├── __init__.py
│   ├── request_parser.py
│   ├── request_extractor.py
│   ├── request_info_adder.py
│   └── mis_id_adder.py
├── __init__.py
└── main.py
```

## 작업 흐름

1. 방화벽 정책 추출 (외부 작업)
2. 중복 정책 추출 (외부 작업)
3. 신청번호 파싱 (태스크 1)
4. 신청번호 추출 (태스크 2)
5. MIS ID 추가 (태스크 3)
6. 신청정보 추가 (태스크 4)
7. 예외처리 (태스크 5 또는 6)
8. 중복정책 분류 (태스크 7)
9. 중복정책 상태 추가 (태스크 8)
10. 미사용 정책 정보 추가 (태스크 9)
11. 정리대상 분류 (태스크 10)

## 로깅

프로그램 실행 중 발생하는 로그는 `firewall_policy_manager.log` 파일에 저장됩니다.