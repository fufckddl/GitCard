import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { fetchProfileCards, ProfileCard, updateProfileCard, deleteProfileCard } from '../api/profileCardApi';
import { PreviewLayout } from '../components/PreviewLayout';
import { BuilderSidebar } from '../components/BuilderSidebar';
import { useProfileConfig } from '../hooks/useProfileConfig';
import { Button } from '../../../shared/components/Button';
import styles from './ProfileCardDetailPage.module.css';

export const ProfileCardDetailPage: React.FC = () => {
  const { cardId } = useParams<{ cardId: string }>();
  const navigate = useNavigate();
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
      profileConfig.updateConfig({
        cardTitle: card.card_title,
        name: card.name,
        title: card.title,
        tagline: card.tagline,
        primaryColor: card.primary_color || '#667eea',
        gradient: card.gradient || `linear-gradient(135deg, ${card.primary_color || '#667eea'} 0%, rgb(102, 126, 234) 100%)`,
        showStacks: card.show_stacks,
        showContact: card.show_contact,
        showGithubStats: card.show_github_stats,
        stacks: card.stacks,
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
      profileConfig.updateConfig({
        cardTitle: card.card_title,
        name: card.name,
        title: card.title,
        tagline: card.tagline,
        primaryColor: card.primary_color || '#667eea',
        gradient: card.gradient || `linear-gradient(135deg, ${card.primary_color || '#667eea'} 0%, rgb(102, 126, 234) 100%)`,
        showStacks: card.show_stacks,
        showContact: card.show_contact,
        showGithubStats: card.show_github_stats,
        stacks: card.stacks,
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
          <div className={styles.previewContainer}>
            <div className={styles.previewWrapper}>
              <PreviewLayout
                config={{
                  cardTitle: card.card_title,
                  name: card.name,
                  title: card.title,
                  tagline: card.tagline,
                  primaryColor: card.primary_color || '#667eea',
                  gradient: card.gradient || `linear-gradient(135deg, ${card.primary_color || '#667eea'} 0%, rgb(102, 126, 234) 100%)`,
                  showStacks: card.show_stacks,
                  showContact: card.show_contact,
                  showGithubStats: card.show_github_stats,
                  stacks: card.stacks,
                  contacts: card.contacts,
                }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

