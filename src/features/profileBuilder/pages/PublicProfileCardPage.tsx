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
    const primaryColor = card.primary_color || '#667eea';
    const secondaryColor = (() => {
      const gradient = card.gradient;
      if (!gradient) {
        return '#764ba2';
      }
      
      // Extract colors in order (both hex and RGB) - same logic as backend
      const colors: string[] = [];
      
      // Helper to normalize hex (3-digit to 6-digit)
      const normalizeHex = (hex: string): string => {
        if (hex.length === 3) {
          return `#${hex[0]}${hex[0]}${hex[1]}${hex[1]}${hex[2]}${hex[2]}`;
        }
        return `#${hex}`;
      };
      
      // Helper to convert RGB to hex
      const rgbToHex = (r: number, g: number, b: number): string => {
        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
      };
      
      // Pattern to match both hex (#...) and rgb(...)
      const colorPattern = /(?:#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})|rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\))/g;
      
      let match;
      while ((match = colorPattern.exec(gradient)) !== null) {
        if (match[1]) {
          // Hex color found
          colors.push(normalizeHex(match[1]));
        } else if (match[2] && match[3] && match[4]) {
          // RGB color found
          const r = parseInt(match[2], 10);
          const g = parseInt(match[3], 10);
          const b = parseInt(match[4], 10);
          colors.push(rgbToHex(r, g, b));
        }
      }
      
      // Extract secondary color
      if (colors.length >= 2) {
        return colors[1];
      } else if (colors.length === 1 && colors[0].toLowerCase() !== primaryColor.toLowerCase()) {
        return colors[0];
      }
      
      return '#764ba2';
    })();

    return {
      cardTitle: card.card_title,
      name: card.name,
      title: card.title,
      tagline: card.tagline,
      primaryColor,
      secondaryColor,
      gradient: card.gradient || `linear-gradient(135deg, ${primaryColor} 0%, ${secondaryColor} 100%)`,
      showStacks: card.show_stacks,
      showContact: card.show_contact,
      showGithubStats: card.show_github_stats,
      showBaekjoon: card.show_baekjoon ?? false,
      baekjoonId: card.baekjoon_id ?? '',
      stackAlignment: card.stack_alignment || 'center',
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




