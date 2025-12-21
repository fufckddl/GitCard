import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { fetchProfileCards, ProfileCard, updateProfileCard, deleteProfileCard } from '../api/profileCardApi';
import { PreviewLayout } from '../components/PreviewLayout';
import { BuilderSidebar } from '../components/BuilderSidebar';
import { MarkdownBadgeSection } from '../components/MarkdownBadgeSection';
import { useProfileConfig } from '../hooks/useProfileConfig';
import { StackBadge } from '../types/profileConfig';
import { Button } from '../../../shared/components/Button';
import { useAuth } from '../../auth/hooks/useAuth';
import styles from './ProfileCardDetailPage.module.css';

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

export const ProfileCardDetailPage: React.FC = () => {
  const { cardId } = useParams<{ cardId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [card, setCard] = useState<ProfileCard | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const profileConfig = useProfileConfig();

  useEffect(() => {
    if (cardId) {
      loadCard();
    }
  }, [cardId]);

  useEffect(() => {
    if (card && !isEditing) {
      // 카드 데이터를 profileConfig에 로드
      const primaryColor = card.primary_color || '#667eea';
      const secondaryColor = (() => {
        const gradient = card.gradient;
        if (!gradient) {
          return '#764ba2';
        }
        
        // 순서대로 색상 추출 (hex와 RGB 모두) - 백엔드와 동일한 로직
        const colors: string[] = [];
        
        // hex 정규화 헬퍼 (3자리를 6자리로)
        const normalizeHex = (hex: string): string => {
          if (hex.length === 3) {
            return `#${hex[0]}${hex[0]}${hex[1]}${hex[1]}${hex[2]}${hex[2]}`;
          }
          return `#${hex}`;
        };
        
        // RGB를 hex로 변환하는 헬퍼
        const rgbToHex = (r: number, g: number, b: number): string => {
          return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
        };
        
        // hex (#...)와 rgb(...) 모두를 매칭하는 패턴
        const colorPattern = /(?:#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})|rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\))/g;
        
        let match;
        while ((match = colorPattern.exec(gradient)) !== null) {
          if (match[1]) {
            // Hex 색상 찾음
            colors.push(normalizeHex(match[1]));
          } else if (match[2] && match[3] && match[4]) {
            // RGB 색상 찾음
            const r = parseInt(match[2], 10);
            const g = parseInt(match[3], 10);
            const b = parseInt(match[4], 10);
            colors.push(rgbToHex(r, g, b));
          }
        }
        
        // 보조 색상 추출
        if (colors.length >= 2) {
          return colors[1];
        } else if (colors.length === 1 && colors[0].toLowerCase() !== primaryColor.toLowerCase()) {
          return colors[0];
        }
        
        return '#764ba2';
      })();
      profileConfig.updateConfig({
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
        stackLabelLang: (card as any).stack_label_lang as 'ko' | 'en' ?? 'en',
        stackAlignment: card.stack_alignment || 'center',
        stacks: convertStacks(card.stacks),
        contacts: card.contacts,
      });
    }
  }, [card, isEditing]);

  const loadCard = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const cards = await fetchProfileCards();
      const foundCard = cards.find((c) => c.id === Number(cardId));
      if (!foundCard) {
        setError('카드를 찾을 수 없습니다.');
        return;
      }
      setCard(foundCard);
    } catch (err) {
      setError(err instanceof Error ? err.message : '카드를 불러오는데 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (!card) return;

    try {
      const updatedCard = await updateProfileCard(card.id, profileConfig.config);
      setCard(updatedCard);
      setIsEditing(false);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : '카드 수정에 실패했습니다.');
    }
  };

  const handleDelete = async () => {
    if (!card) return;

    if (!window.confirm('정말로 이 카드를 삭제하시겠습니까?')) {
      return;
    }

    try {
      await deleteProfileCard(card.id);
      navigate('/dashboard/cards');
    } catch (err) {
      setError(err instanceof Error ? err.message : '카드 삭제에 실패했습니다.');
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    if (card) {
      const primaryColor = card.primary_color || '#667eea';
      const secondaryColor = (() => {
        const gradient = card.gradient;
        if (!gradient) {
          return '#764ba2';
        }
        const hexRegex = /#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})/g;
        const matches = gradient.match(hexRegex);
        if (matches && matches.length >= 2) {
          return matches[1];
        }
        if (matches && matches.length === 1 && matches[0].toLowerCase() !== primaryColor.toLowerCase()) {
          return matches[0];
        }
        return '#764ba2';
      })();
      profileConfig.updateConfig({
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
        stackLabelLang: (card as any).stack_label_lang as 'ko' | 'en' ?? 'en',
        stackAlignment: card.stack_alignment || 'center',
        stacks: convertStacks(card.stacks),
        contacts: card.contacts,
      });
    }
    setIsEditing(false);
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>로딩 중...</div>
      </div>
    );
  }

  if (error && !card) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error}</div>
        <Button onClick={() => navigate('/dashboard/cards')} variant="primary">
          목록으로 돌아가기
        </Button>
      </div>
    );
  }

  if (!card) {
    return null;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.headerLeft}>
          <Button onClick={() => navigate('/dashboard/cards')} variant="secondary">
            ← 목록
          </Button>
          {!isEditing ? (
            <div className={styles.titleSection}>
              <h1 className={styles.title}>{card.card_title}</h1>
              <div className={styles.cardTitleEdit}>
                <label className={styles.cardTitleLabel}>카드 제목 (목록용)</label>
                <input
                  type="text"
                  value={profileConfig.config.cardTitle}
                  onChange={(e) => profileConfig.updateConfig({ cardTitle: e.target.value })}
                  className={styles.titleInput}
                  placeholder="카드 제목"
                />
              </div>
            </div>
          ) : (
            <div className={styles.cardTitleEdit}>
              <label className={styles.cardTitleLabel}>카드 제목 (목록용)</label>
              <input
                type="text"
                value={profileConfig.config.cardTitle}
                onChange={(e) => profileConfig.updateConfig({ cardTitle: e.target.value })}
                className={styles.titleInputEdit}
                placeholder="카드 제목"
              />
            </div>
          )}
        </div>
        <div className={styles.headerActions}>
          {!isEditing ? (
            <>
              <Button onClick={handleEdit} variant="primary">
                수정
              </Button>
              <Button onClick={handleDelete} variant="secondary">
                삭제
              </Button>
            </>
          ) : (
            <>
              <Button onClick={handleCancel} variant="secondary">
                취소
              </Button>
              <Button onClick={handleSave} variant="primary">
                저장
              </Button>
            </>
          )}
        </div>
      </div>

      {error && (
        <div className={styles.errorMessage}>{error}</div>
      )}

      <div className={styles.content}>
        {isEditing ? (
          <div className={styles.editorContainer}>
            <BuilderSidebar profileConfig={profileConfig} />
            <div className={styles.previewContainer}>
              <div className={styles.previewWrapper}>
                <PreviewLayout config={profileConfig.config} />
              </div>
            </div>
          </div>
        ) : (
          <>
          <div className={styles.previewContainer}>
            <div className={styles.previewWrapper}>
              <PreviewLayout
                config={{
                  cardTitle: card.card_title,
                  name: card.name,
                  title: card.title,
                  tagline: card.tagline,
                  primaryColor: card.primary_color || '#667eea',
                    secondaryColor: '#764ba2',
                    gradient:
                      card.gradient ||
                      `linear-gradient(135deg, ${card.primary_color || '#667eea'} 0%, #764ba2 100%)`,
                  showStacks: card.show_stacks,
                  showContact: card.show_contact,
                  showGithubStats: card.show_github_stats,
                    showBaekjoon: card.show_baekjoon ?? false,
                    baekjoonId: card.baekjoon_id ?? '',
                    stackLabelLang: (card as any).stack_label_lang as 'ko' | 'en' ?? 'en',
                    stackAlignment: card.stack_alignment || 'center',
                    stacks: convertStacks(card.stacks),
                  contacts: card.contacts,
                }}
              />
            </div>
          </div>
            {user?.github_login && (
              <MarkdownBadgeSection
                githubLogin={user.github_login}
                cardId={card.id}
              />
            )}
          </>
        )}
      </div>
    </div>
  );
};

