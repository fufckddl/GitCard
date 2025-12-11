import { getToken } from '../../../shared/utils/storage';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface GitHubStats {
  repositories: number;
  stars: number;
  followers: number;
  following: number;
  contributions: number | null;
}

export const fetchGitHubStats = async (): Promise<GitHubStats> => {
  const token = getToken();
  if (!token) {
    throw new Error('인증이 필요합니다.');
  }

  const response = await fetch(`${API_BASE_URL}/api/users/me/github-stats`, {
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
    throw new Error('GitHub 통계를 가져오는데 실패했습니다.');
  }

  return response.json();
};

