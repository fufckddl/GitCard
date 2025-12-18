import React from 'react';
import { ProfileConfig } from '../types/profileConfig';
import styles from './BaekjoonSection.module.css';

interface BaekjoonSectionProps {
  config: ProfileConfig;
}

export const BaekjoonSection: React.FC<BaekjoonSectionProps> = ({ config }) => {
  if (!config.showBaekjoon || !config.baekjoonId) {
    return null;
  }

  const handle = config.baekjoonId.trim();
  const badgeSrc = `http://mazassumnida.wtf/api/v2/generate_badge?boj=${encodeURIComponent(handle)}`;
  const profileUrl = `https://solved.ac/${encodeURIComponent(handle)}`;

  return (
    <div className={styles.section}>
      <h2 className={styles.sectionTitle}>Baekjoon</h2>
      <div className={styles.content}>
        <a href={profileUrl} target="_blank" rel="noopener noreferrer">
          <img src={badgeSrc} alt="Solved.ac Profile" className={styles.badge} />
        </a>
      </div>
    </div>
  );
};
