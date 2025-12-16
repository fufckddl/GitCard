# 이미지 잘림 문제 해결 가이드

## 문제 원인 분석

### 현재 구조
```
.container (배경 그라데이션, padding: 40px)
  └── .cardWrapper (max-width: 800px, white background)
      └── [data-testid="gitcard-root"] (PreviewLayout, 실제 카드 내용)
```

### 잠재적 문제점

1. **clip 파라미터 사용 문제**
   - `element.screenshot(clip={...})`를 사용하면 요소의 bounding box를 제한할 수 있음
   - `element.screenshot()`은 이미 요소의 전체 bounding box를 자동으로 캡처함
   - clip을 추가로 지정하면 잘릴 수 있음

2. **뷰포트 높이 부족**
   - 카드가 뷰포트 밖에 있으면 스크린샷이 잘릴 수 있음
   - 동적으로 높이를 조정해도 타이밍 문제로 잘릴 수 있음

3. **스크롤 위치 문제**
   - 요소가 스크롤된 위치에 있으면 일부가 잘릴 수 있음
   - `scroll_into_view_if_needed()`가 제대로 작동하지 않을 수 있음

4. **렌더링 타이밍 문제**
   - JavaScript로 높이를 측정하지만, 그 사이에 레이아웃이 변경될 수 있음
   - 비동기 콘텐츠(이미지, 폰트) 로딩이 완료되기 전에 스크린샷을 찍을 수 있음

## 해결 방안

### 방안 1: clip 제거 + full_page 스크린샷 후 crop (권장)

```python
# clip을 제거하고 element.screenshot()만 사용
screenshot = await card_element.screenshot(type=format)
```

### 방안 2: 전체 페이지 스크린샷 후 카드 영역만 crop

```python
# 전체 페이지를 스크린샷
full_screenshot = await page.screenshot(type=format, full_page=True)
# 카드 요소의 위치를 찾아서 crop (PIL 사용)
```

### 방안 3: 카드 요소를 별도 페이지로 렌더링

```python
# 카드만 포함하는 최소 HTML 페이지 생성
# 배경 제거, 패딩 제거
```

## 테스트 전 확인 사항

1. **로컬 테스트 환경 설정**
   ```bash
   # 백엔드 서버 실행
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   
   # 프론트엔드 서버 실행
   npm run dev
   ```

2. **테스트 URL 확인**
   - `http://localhost:5173/dashboard/{github_login}/cards/{card_id}`
   - 브라우저에서 직접 열어서 카드가 완전히 보이는지 확인

3. **Playwright 디버그 모드**
   ```python
   # headless=False로 실행하여 실제 브라우저 창 확인
   browser = await p.chromium.launch(headless=False)
   ```

4. **스크린샷 저장 확인**
   ```python
   # 스크린샷을 파일로 저장하여 확인
   with open("debug_screenshot.png", "wb") as f:
       f.write(screenshot)
   ```

## 권장 수정 사항

1. **clip 파라미터 제거**: `element.screenshot()`만 사용
2. **충분한 대기 시간**: 모든 콘텐츠가 로드될 때까지 충분히 대기
3. **뷰포트를 충분히 크게**: 최소 3000px 높이로 설정
4. **스크롤 처리**: 페이지를 맨 위로 스크롤한 후 요소로 스크롤
