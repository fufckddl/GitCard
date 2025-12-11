import React from 'react';
import { ProfileConfig } from '../types/profileConfig';
import { useGitHubStats } from '../hooks/useGitHubStats';
import styles from './GithubStatsSection.module.css';

interface GithubStatsSectionProps {
  config: ProfileConfig;
}

export const GithubStatsSection: React.FC<GithubStatsSectionProps> = ({ config }) => {
  const { stats, isLoading, error } = useGitHubStats();
  
  // 선택한 색상 기반으로 그라데이션 생성
  const getGradientStyle = () => {
    // config.gradient에서 색상 추출하거나 직접 생성
    if (config.gradient) {
      return { background: config.gradient };
    }
    // fallback: 기본 그라데이션
    return { background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' };
  };

  if (!config.showGithubStats) {
    return null;
  }

  if (isLoading) {
    return (
      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Github-stats</h2>
        <div className={styles.loading}>로딩 중...</div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Github-stats</h2>
        <div className={styles.error}>
          {error || '통계를 불러올 수 없습니다.'}
        </div>
      </div>
    );
  }

  const gradientStyle = getGradientStyle();

  return (
    <div className={styles.section}>
      <h2 className={styles.sectionTitle}>Github-stats</h2>
      <div className={styles.content}>
        {stats.contributions !== null && (
          <div className={styles.statCard} style={gradientStyle}>
            <div className={styles.statValue}>{stats.contributions.toLocaleString()}</div>
            <div className={styles.statLabel}>Contributions</div>
          </div>
        )}
        <div className={styles.statCard} style={gradientStyle}>
          <div className={styles.statValue}>{stats.repositories}</div>
          <div className={styles.statLabel}>Repositories</div>
        </div>
        <div className={styles.statCard} style={gradientStyle}>
          <div className={styles.statValue}>{stats.stars.toLocaleString()}</div>
          <div className={styles.statLabel}>Stars</div>
        </div>
        <div className={styles.statCard} style={gradientStyle}>
          <div className={styles.statValue}>{stats.followers}</div>
          <div className={styles.statLabel}>Followers</div>
        </div>
        <div className={styles.statCard} style={gradientStyle}>
          <div className={styles.statValue}>{stats.following}</div>
          <div className={styles.statLabel}>Following</div>
        </div>
      </div>
    </div>
  );
};

