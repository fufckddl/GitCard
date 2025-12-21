"""
OAuth 흐름을 위한 임시 인메모리 state 저장소.

보안 참고: `state` 매개변수는 CSRF 공격을 방지하는 데 사용됩니다.
랜덤 state 값을 생성하고 서버 측에 저장한 다음,
GitHub가 콜백 엔드포인트로 리다이렉트할 때 검증합니다.

프로덕션에서는 다음으로 교체하세요:
- Redis (분산 시스템에 권장)
- 서버 측 세션 저장소 (예: Flask-Session, FastAPI-Session)
- 데이터베이스 기반 세션 저장소

state는 합리적인 시간(예: 10분) 후에 만료되어야 합니다.
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional


# 인메모리 state 저장소
# 키: state (str), 값: 생성 타임스탬프 (datetime)
_state_store: Dict[str, datetime] = {}

# State 만료 시간 (10분)
STATE_EXPIRATION_MINUTES = 10


def generate_state() -> str:
    """
    OAuth 흐름을 위한 랜덤 state 값을 생성합니다.
    
    Returns:
        OAuth state 매개변수로 사용할 UUID 문자열.
    """
    state = str(uuid.uuid4())
    _state_store[state] = datetime.utcnow()
    return state


def validate_state(state: str) -> bool:
    """
    state가 존재하고 만료되지 않았는지 검증합니다.
    
    Args:
        state: 검증할 state 값
        
    Returns:
        state가 유효하면 True, 그렇지 않으면 False
    """
    if state not in _state_store:
        return False
    
    # 만료 확인
    created_at = _state_store[state]
    expiration_time = created_at + timedelta(minutes=STATE_EXPIRATION_MINUTES)
    
    if datetime.utcnow() > expiration_time:
        # state 만료됨, 제거
        del _state_store[state]
        return False
    
    # state가 유효함, 제거 (일회용)
    del _state_store[state]
    return True


def cleanup_expired_states():
    """
    저장소에서 만료된 state를 제거합니다.
    프로덕션에서는 주기적으로 호출하세요 (예: 백그라운드 작업을 통해).
    """
    now = datetime.utcnow()
    expired_states = [
        state
        for state, created_at in _state_store.items()
        if now > created_at + timedelta(minutes=STATE_EXPIRATION_MINUTES)
    ]
    for state in expired_states:
        del _state_store[state]

