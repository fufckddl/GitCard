import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useProfileConfig } from '../hooks/useProfileConfig';
import { PreviewLayout } from '../components/PreviewLayout';
import { BuilderSidebar } from '../components/BuilderSidebar';
import { saveProfileCard } from '../api/profileCardApi';
import { Button } from '../../../shared/components/Button';
import styles from '../styles/ProfileBuilderPage.module.css';

export const ProfileBuilderPage: React.FC = () => {
  const profileConfig = useProfileConfig();
  const navigate = useNavigate();
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  const handleSave = async () => {
    try {
      setIsSaving(true);
      setSaveMessage(null);
      await saveProfileCard(profileConfig.config);
      setSaveMessage('저장되었습니다!');
      setTimeout(() => {
        setSaveMessage(null);
        navigate('/dashboard/cards');
      }, 1500);
    } catch (error) {
      setSaveMessage(error instanceof Error ? error.message : '저장에 실패했습니다.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className={styles.container}>
      <BuilderSidebar profileConfig={profileConfig} />
      <div className={styles.previewContainer}>
        <div className={styles.previewHeader}>
          <div className={styles.headerLeft}>
            <h2 className={styles.previewTitle}>미리보기</h2>
            <div className={styles.cardTitleSection}>
              <label className={styles.cardTitleLabel}>카드 제목 (목록용)</label>
              <input
                type="text"
                value={profileConfig.config.cardTitle}
                onChange={(e) => profileConfig.updateConfig({ cardTitle: e.target.value })}
                className={styles.cardTitleInput}
                placeholder="카드 제목"
              />
            </div>
          </div>
          <div className={styles.saveSection}>
            {saveMessage && (
              <span className={saveMessage.includes('실패') ? styles.errorMessage : styles.successMessage}>
                {saveMessage}
              </span>
            )}
            <Button
              onClick={handleSave}
              variant="primary"
              disabled={isSaving}
            >
              {isSaving ? '저장 중...' : '저장'}
            </Button>
          </div>
        </div>
        <div className={styles.previewWrapper}>
          <PreviewLayout config={profileConfig.config} />
        </div>
      </div>
    </div>
  );
};

