import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchPublicProfileCard, ProfileCard } from '../api/profileCardApi';
import { PreviewLayout } from '../components/PreviewLayout';
import { ProfileConfig, StackBadge } from '../types/profileConfig';
import styles from './PublicProfileCardPage.module.css';

// API에서 받은 stacks를 StackBadge[]로 변환
const convertStacks = (stacks: ProfileCard['stacks']): StackBadge[] => {
  return stacks.map(stack => ({
    id: stack.id,
    key: stack.key || stack.id, // key가 없으면 id 사용
    label: stack.label,
    category: stack.category,
    color: stack.color,
  }));
};

export const PublicProfileCardPage: React.FC = () => {
  const { githubLogin, cardId } = useParams<{ githubLogin: string; cardId: string }>();
  const navigate = useNavigate();
  const [card, setCard] = useState<ProfileCard | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!githubLogin || !cardId) {
      setError('잘못된 경로입니다.');
      setIsLoading(false);
      return;
    }

    loadCard();
  }, [githubLogin, cardId]);

  const loadCard = async () => {
    if (!githubLogin || !cardId) return;

    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchPublicProfileCard(githubLogin, parseInt(cardId, 10));
      setCard(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '카드를 불러오는데 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const convertToProfileConfig = (card: ProfileCard): ProfileConfig => {
    return {
      cardTitle: card.card_title,
      name: card.name,
      title: card.title,
      tagline: card.tagline,
      primaryColor: card.primary_color || '#667eea',
      gradient: card.gradient,
      showStacks: card.show_stacks,
      showContact: card.show_contact,
      showGithubStats: card.show_github_stats,
      stacks: convertStacks(card.stacks),
      contacts: card.contacts,
    };
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>로딩 중...</div>
      </div>
    );
  }

  if (error || !card) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error || '카드를 찾을 수 없습니다.'}</div>
        <button onClick={() => navigate('/')} className={styles.backButton}>
          홈으로 돌아가기
        </button>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.cardWrapper}>
        <PreviewLayout config={convertToProfileConfig(card)} />
      </div>
    </div>
  );
};




