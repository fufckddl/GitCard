import React from 'react';
import { ProfileConfig } from '../types/profileConfig';
import { BannerSection } from './BannerSection';
import { StacksSection } from './StacksSection';
import { ContactSection } from './ContactSection';
import { GithubStatsSection } from './GithubStatsSection';
import { BaekjoonSection } from './BaekjoonSection';
import styles from './PreviewLayout.module.css';

interface PreviewLayoutProps {
  config: ProfileConfig;
}

export const PreviewLayout: React.FC<PreviewLayoutProps> = ({ config }) => {
  return (
    <div className={styles.container} data-testid="gitcard-root">
      <BannerSection config={config} />
      {config.showStacks && <StacksSection config={config} />}
      {config.showContact && <ContactSection config={config} />}
      {config.showBaekjoon && config.baekjoonId && (
        <BaekjoonSection config={config} />
      )}
      {config.showGithubStats && <GithubStatsSection config={config} />}
    </div>
  );
};
