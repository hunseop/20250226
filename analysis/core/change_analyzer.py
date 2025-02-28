"""
정책 변경사항 분석을 위한 클래스입니다.
"""

import pandas as pd
import logging
from typing import Dict, List, Set
from datetime import datetime

class ChangeAnalyzer:
    """정책 변경사항 분석을 위한 클래스"""
    
    def __init__(self):
        """ChangeAnalyzer 초기화"""
        self.logger = logging.getLogger(__name__)
        self.ignore_columns = {'Seq', '_merge'}
    
    def _find_added_policies(self, 
                           df_merged: pd.DataFrame) -> pd.DataFrame:
        """
        추가된 정책을 찾습니다.
        
        Args:
            df_merged: 병합된 데이터프레임
        
        Returns:
            추가된 정책 데이터프레임
        """
        added = df_merged[df_merged['_merge'] == 'right_only']
        added_cols = ['Rule Name'] + [col for col in added.columns 
                                    if col.endswith('_after') 
                                    and not col.startswith('Seq')]
        return added[added_cols].rename(
            columns=lambda x: x.replace('_after', '')
        )
    
    def _find_removed_policies(self, 
                             df_merged: pd.DataFrame) -> pd.DataFrame:
        """
        제거된 정책을 찾습니다.
        
        Args:
            df_merged: 병합된 데이터프레임
        
        Returns:
            제거된 정책 데이터프레임
        """
        removed = df_merged[df_merged['_merge'] == 'left_only']
        removed_cols = ['Rule Name'] + [col for col in removed.columns 
                                      if col.endswith('_before')
                                      and not col.startswith('Seq')]
        return removed[removed_cols].rename(
            columns=lambda x: x.replace('_before', '')
        )
    
    def _find_changed_policies(self, 
                             df_merged: pd.DataFrame) -> pd.DataFrame:
        """
        변경된 정책을 찾습니다.
        
        Args:
            df_merged: 병합된 데이터프레임
        
        Returns:
            변경된 정책 데이터프레임
        """
        # 공통 컬럼 찾기 (Seq와 _merge 제외)
        common_cols = [col.replace('_before', '') 
                      for col in df_merged.columns 
                      if col.endswith('_before')
                      and not col.startswith('Seq')]
        
        # 변경 조건 생성
        change_conditions = [
            df_merged[f'{col}_before'] != df_merged[f'{col}_after']
            for col in common_cols
        ]
        
        # 변경된 정책 필터링
        changed = df_merged[
            (df_merged['_merge'] == 'both') & 
            pd.concat(change_conditions, axis=1).any(axis=1)
        ]
        
        # 변경 내역 생성
        changes_list = []
        for idx, row in changed.iterrows():
            changes = {'Rule Name': row['Rule Name']}
            for col in common_cols:
                if row[f'{col}_before'] != row[f'{col}_after']:
                    changes[f'{col}_before'] = row[f'{col}_before']
                    changes[f'{col}_after'] = row[f'{col}_after']
            changes_list.append(changes)
        
        return pd.DataFrame(changes_list)
    
    def analyze(self, 
                df_before: pd.DataFrame,
                df_after: pd.DataFrame,
                **kwargs) -> Dict[str, pd.DataFrame]:
        """
        정책 변경사항을 분석합니다.
        
        Args:
            df_before: 이전 정책 데이터프레임
            df_after: 현재 정책 데이터프레임
            **kwargs: 추가 매개변수
        
        Returns:
            분석 결과를 담은 딕셔너리
            - added: 추가된 정책
            - removed: 제거된 정책
            - changed: 변경된 정책
        """
        try:
            self.logger.info("정책 변경사항 분석 시작")
            
            # 데이터프레임 병합
            df_merged = df_before.merge(
                df_after,
                on='Rule Name',
                how='outer',
                suffixes=('_before', '_after'),
                indicator=True
            )
            
            # 변경사항 분석
            added = self._find_added_policies(df_merged)
            removed = self._find_removed_policies(df_merged)
            changed = self._find_changed_policies(df_merged)
            
            self.logger.info(
                f"분석 완료 - 추가: {len(added)}개, "
                f"제거: {len(removed)}개, "
                f"변경: {len(changed)}개"
            )
            
            return {
                'added': added,
                'removed': removed,
                'changed': changed
            }
            
        except Exception as e:
            self.logger.error(f"변경사항 분석 중 오류 발생: {e}")
            raise 