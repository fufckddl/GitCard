import React from 'react';
import { ProfileConfig } from '../types/profileConfig';
import styles from './RepositoriesSection.module.css';

interface RepositoriesSectionProps {
  config: ProfileConfig;
}

export const RepositoriesSection: React.FC<RepositoriesSectionProps> = ({ config }) => {
  if (!config.repositories || config.repositories.length === 0) {
    return null;
  }

  return (
    <div className={styles.section}>
      <h2 className={styles.sectionTitle}>Repositories</h2>
      <div className={styles.repositoriesGrid}>
        {config.repositories.map((repo, index) => (
          <a
            key={index}
            href={repo.html_url}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.repoCard}
          >
            <div className={styles.repoHeader}>
              <h3 className={styles.repoName}>{repo.name}</h3>
              {repo.language && (
                <span className={styles.language}>{repo.language}</span>
              )}
            </div>
            {repo.description && (
              <p className={styles.repoDescription}>{repo.description}</p>
            )}
            <div className={styles.repoStats}>
              <span className={styles.stat}>
                ⭐ {repo.stargazers_count}
              </span>
              <span className={styles.stat}>
                🍴 {repo.forks_count}
              </span>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};
