import React from 'react';
import { GitHubLoginCard } from '../components/GitHubLoginCard';
import styles from './LoginPage.module.css';

export const LoginPage: React.FC = () => {
  return (
    <div className={styles.container}>
      <GitHubLoginCard />
    </div>
  );
};

