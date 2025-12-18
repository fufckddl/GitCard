import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchProfileCards, ProfileCard, deleteProfileCard } from '../api/profileCardApi';
import { PreviewLayout } from '../components/PreviewLayout';
import { MarkdownBadgeSection } from '../components/MarkdownBadgeSection';
import { ProfileConfig, StackBadge } from '../types/profileConfig';
import { Button } from '../../../shared/components/Button';
import { useAuth } from '../../auth/hooks/useAuth';
import styles from './ProfileCardListPage.module.css';

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

export const ProfileCardListPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [cards, setCards] = useState<ProfileCard[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCard, setSelectedCard] = useState<ProfileCard | null>(null);

  useEffect(() => {
    loadCards();
  }, []);

  const loadCards = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchProfileCards();
      setCards(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '카드 목록을 불러오는데 실패했습니다.');
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

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const handleDelete = async (cardId: number, e: React.MouseEvent) => {
    e.stopPropagation(); // 카드 클릭 이벤트 방지
    if (!window.confirm('정말로 이 카드를 삭제하시겠습니까?')) {
      return;
    }

    try {
      await deleteProfileCard(cardId);
      await loadCards(); // 목록 새로고침
      if (selectedCard?.id === cardId) {
        setSelectedCard(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '카드 삭제에 실패했습니다.');
    }
  };

  const handleEdit = (cardId: number, e: React.MouseEvent) => {
    e.stopPropagation(); // 카드 클릭 이벤트 방지
    navigate(`/dashboard/cards/${cardId}`);
  };

  const handleViewCard = (cardId: number, e: React.MouseEvent) => {
    e.stopPropagation(); // 카드 클릭 이벤트 방지
    if (user?.github_login) {
      navigate(`/dashboard/${user.github_login}/cards/${cardId}`);
    } else {
      alert('GitHub 로그인 정보를 찾을 수 없습니다.');
    }
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>로딩 중...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error}</div>
        <Button onClick={loadCards} variant="primary">
          다시 시도
        </Button>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>내 프로필 카드</h1>
        <Button onClick={() => navigate('/builder')} variant="primary">
          새 카드 만들기
        </Button>
      </div>

      {cards.length === 0 ? (
        <div className={styles.emptyState}>
          <p>아직 생성한 카드가 없습니다.</p>
          <Button onClick={() => navigate('/builder')} variant="primary">
            첫 카드 만들기
          </Button>
        </div>
      ) : (
        <div className={styles.content}>
          <div className={styles.cardList}>
            {cards.map((card) => (
              <div
                key={card.id}
                className={`${styles.cardItem} ${selectedCard?.id === card.id ? styles.selected : ''}`}
                onClick={() => setSelectedCard(card)}
              >
                <div className={styles.cardHeader}>
                  <div className={styles.cardHeaderLeft}>
                    <h3 className={styles.cardName}>{card.card_title || card.title}</h3>
                    <span className={styles.cardTitle}>{card.title}</span>
                  </div>
                  <div className={styles.cardActions} onClick={(e) => e.stopPropagation()}>
                    <Button
                      onClick={(e) => {
                        e?.stopPropagation();
                        handleViewCard(card.id, e!);
                      }}
                      variant="primary"
                      type="button"
                    >
                      카드보기
                    </Button>
                    <Button
                      onClick={(e) => {
                        e?.stopPropagation();
                        handleEdit(card.id, e!);
                      }}
                      variant="secondary"
                      type="button"
                    >
                      수정
                    </Button>
                    <Button
                      onClick={(e) => {
                        e?.stopPropagation();
                        handleDelete(card.id, e!);
                      }}
                      variant="secondary"
                      type="button"
                    >
                      삭제
                    </Button>
                  </div>
                </div>
                <p className={styles.cardTagline}>{card.tagline}</p>
                <div className={styles.cardMeta}>
                  <span>스택: {card.stacks.length}개</span>
                  <span>연락처: {card.contacts.length}개</span>
                </div>
                <div className={styles.cardDate}>
                  생성: {formatDate(card.created_at)}
                </div>
              </div>
            ))}
          </div>

          {selectedCard && (
            <div className={styles.previewSection}>
              <h2 className={styles.previewTitle}>미리보기</h2>
              <div className={styles.previewWrapper}>
                <PreviewLayout config={convertToProfileConfig(selectedCard)} />
              </div>
              {user?.github_login && (
                <MarkdownBadgeSection
                  githubLogin={user.github_login}
                  cardId={selectedCard.id}
                />
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

