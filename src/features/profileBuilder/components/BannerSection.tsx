import React from 'react';
import { ProfileConfig } from '../types/profileConfig';
import styles from './BannerSection.module.css';

interface BannerSectionProps {
  config: ProfileConfig;
}

export const BannerSection: React.FC<BannerSectionProps> = ({ config }) => {
  const gradientStyle = {
    background: config.gradient,
  };

  return (
    <div className={styles.banner} style={gradientStyle}>
      <div className={styles.content}>
        <h1 className={styles.greeting}>
          Hello World 👋 I'm {config.name}!
        </h1>
        <p className={styles.title}>{config.title}</p>
        {config.tagline && (
          <p className={styles.tagline}>{config.tagline}</p>
        )}
      </div>
    </div>
  );
};

