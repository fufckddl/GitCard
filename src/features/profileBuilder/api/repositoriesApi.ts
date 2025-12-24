import { getToken } from '../../../shared/utils/storage';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface GitHubRepository {
  name: string;
  description: string;
  html_url: string;
  language?: string;
  stargazers_count: number;
  forks_count: number;
  updated_at?: string;
}

export interface RepositoriesResponse {
  repositories: GitHubRepository[];
  count: number;
}

export const fetchRepositories = async (): Promise<RepositoriesResponse> => {
  const token = getToken();
  if (!token) {
    throw new Error('인증이 필요합니다.');
  }

  const response = await fetch(`${API_BASE_URL}/users/me/repositories`, {
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
    throw new Error('레포지토리 목록을 가져오는데 실패했습니다.');
  }

  return response.json();
};
