const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface VisitorStats {
  today_visitors: number;
  total_visitors: number;
}

export const fetchVisitorStats = async (): Promise<VisitorStats> => {
  const response = await fetch(`${API_BASE_URL}/dashboard/stats`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('접속자 통계를 가져오는데 실패했습니다.');
  }

  return response.json();
};

export const recordVisit = async (): Promise<VisitorStats> => {
  const response = await fetch(`${API_BASE_URL}/dashboard/visit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('접속 기록에 실패했습니다.');
  }

  return response.json();
};


