import { User } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const fetchCurrentUser = async (token: string): Promise<User> => {
  const response = await fetch(`${API_BASE_URL}/api/users/me`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('인증이 만료되었습니다. 다시 로그인해주세요.');
    }
    throw new Error('사용자 정보를 가져오는데 실패했습니다.');
  }

  return response.json();
};

