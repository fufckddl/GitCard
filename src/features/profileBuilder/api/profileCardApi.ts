import { getToken } from '../../../shared/utils/storage';
import { ProfileConfig } from '../types/profileConfig';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface ProfileCard {
  id: number;
  user_id: number;
  card_title: string;    // 카드 목록에서 보이는 제목
  name: string;
  title: string;         // 프로필 카드에 표시되는 제목
  tagline: string;
  primary_color: string; // 카드의 주요 색상 (hex color) - UI에서 선택용
  gradient: string;      // 배너에 사용할 그라데이션 문자열
  show_stacks: boolean;
  show_contact: boolean;
  show_github_stats: boolean;
  show_baekjoon?: boolean;
  baekjoon_id?: string | null;
  stack_alignment: 'left' | 'center' | 'right';  // 스택 배지 정렬
  stacks: Array<{ id: string; key?: string; label: string; category: string; color: string }>;
  contacts: Array<{ id: string; label: string; value: string; type?: string }>;
  created_at: string;
  updated_at: string;
}

export const saveProfileCard = async (config: ProfileConfig): Promise<ProfileCard> => {
  const token = getToken();
  if (!token) {
    throw new Error('인증이 필요합니다.');
  }

  const response = await fetch(`${API_BASE_URL}/profiles`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      card_title: config.cardTitle,
      name: config.name,
      title: config.title,
      tagline: config.tagline,
      primary_color: config.primaryColor,
      gradient: config.gradient,
      show_stacks: config.showStacks,
      show_contact: config.showContact,
      show_github_stats: config.showGithubStats,
      show_baekjoon: config.showBaekjoon,
      baekjoon_id: config.baekjoonId,
      stack_alignment: config.stackAlignment,
      stacks: config.stacks,
      contacts: config.contacts,
    }),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('인증이 만료되었습니다. 다시 로그인해주세요.');
    }
    const error = await response.json().catch(() => ({ detail: '프로필 카드 저장에 실패했습니다.' }));
    throw new Error(error.detail || '프로필 카드 저장에 실패했습니다.');
  }

  return response.json();
};

export const fetchProfileCards = async (): Promise<ProfileCard[]> => {
  const token = getToken();
  if (!token) {
    throw new Error('인증이 필요합니다.');
  }

  const response = await fetch(`${API_BASE_URL}/profiles`, {
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
    throw new Error('프로필 카드 목록을 가져오는데 실패했습니다.');
  }

  return response.json();
};

export const updateProfileCard = async (
  cardId: number,
  config: ProfileConfig
): Promise<ProfileCard> => {
  const token = getToken();
  if (!token) {
    throw new Error('인증이 필요합니다.');
  }

  const response = await fetch(`${API_BASE_URL}/profiles/${cardId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      card_title: config.cardTitle,
      name: config.name,
      title: config.title,
      tagline: config.tagline,
      primary_color: config.primaryColor,
      gradient: config.gradient,
      show_stacks: config.showStacks,
      show_contact: config.showContact,
      show_github_stats: config.showGithubStats,
      show_baekjoon: config.showBaekjoon,
      baekjoon_id: config.baekjoonId,
      stack_alignment: config.stackAlignment,
      stacks: config.stacks,
      contacts: config.contacts,
    }),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('인증이 만료되었습니다. 다시 로그인해주세요.');
    }
    if (response.status === 404) {
      throw new Error('프로필 카드를 찾을 수 없습니다.');
    }
    const error = await response.json().catch(() => ({ detail: '프로필 카드 수정에 실패했습니다.' }));
    throw new Error(error.detail || '프로필 카드 수정에 실패했습니다.');
  }

  return response.json();
};

export const deleteProfileCard = async (cardId: number): Promise<void> => {
  const token = getToken();
  if (!token) {
    throw new Error('인증이 필요합니다.');
  }

  const response = await fetch(`${API_BASE_URL}/profiles/${cardId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('인증이 만료되었습니다. 다시 로그인해주세요.');
    }
    if (response.status === 404) {
      throw new Error('프로필 카드를 찾을 수 없습니다.');
    }
    throw new Error('프로필 카드 삭제에 실패했습니다.');
  }
};

/**
 * 공개 프로필 카드 조회 (인증 불필요)
 * @param githubLogin GitHub 사용자명
 * @param cardId 카드 ID
 */
export const fetchPublicProfileCard = async (
  githubLogin: string,
  cardId: number
): Promise<ProfileCard> => {
  const response = await fetch(
    `${API_BASE_URL}/profiles/public/${githubLogin}/cards/${cardId}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('프로필 카드를 찾을 수 없습니다.');
    }
    throw new Error('프로필 카드를 불러오는데 실패했습니다.');
  }

  return response.json();
};
