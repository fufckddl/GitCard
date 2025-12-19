const TOKEN_KEY = 'auth_token';
const VISIT_DATE_KEY = 'gitcard_visit_date';

export const setToken = (token: string): void => {
  localStorage.setItem(TOKEN_KEY, token);
};

export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

export const clearToken = (): void => {
  localStorage.removeItem(TOKEN_KEY);
};

/**
 * 한국 시간(KST, UTC+9) 기준으로 오늘 날짜를 YYYY-MM-DD 형식으로 반환
 */
export const getKoreaDateString = (): string => {
  const now = new Date();
  // UTC 시간에 9시간을 더해 한국 시간으로 변환
  const koreaTime = new Date(now.getTime() + (9 * 60 * 60 * 1000));
  const year = koreaTime.getUTCFullYear();
  const month = String(koreaTime.getUTCMonth() + 1).padStart(2, '0');
  const day = String(koreaTime.getUTCDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

/**
 * 오늘 이미 접속 기록이 있는지 확인
 * @returns true if already visited today, false otherwise
 */
export const hasVisitedToday = (): boolean => {
  const today = getKoreaDateString();
  const lastVisitDate = localStorage.getItem(VISIT_DATE_KEY);
  return lastVisitDate === today;
};

/**
 * 오늘 접속 기록 저장
 */
export const markVisitedToday = (): void => {
  const today = getKoreaDateString();
  localStorage.setItem(VISIT_DATE_KEY, today);
};

