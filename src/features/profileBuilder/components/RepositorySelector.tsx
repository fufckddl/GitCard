import React, { useEffect, useState } from 'react';
import { fetchRepositories, GitHubRepository } from '../api/repositoriesApi';
import styles from './RepositorySelector.module.css';

interface RepositorySelectorProps {
  selectedRepositories: Array<{
    name: string;
    description: string;
    html_url: string;
    language?: string;
    stargazers_count: number;
    forks_count: number;
  }>;
  onSelect: (repositories: Array<{
    name: string;
    description: string;
    html_url: string;
    language?: string;
    stargazers_count: number;
    forks_count: number;
  }>) => void;
  onClose: () => void;
}

export const RepositorySelector: React.FC<RepositorySelectorProps> = ({
  selectedRepositories,
  onSelect,
  onClose,
}) => {
  const [repositories, setRepositories] = useState<GitHubRepository[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<Set<string>>(
    new Set(selectedRepositories.map((repo) => repo.name))
  );

  useEffect(() => {
    const loadRepositories = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await fetchRepositories(8);
        setRepositories(data.repositories);
      } catch (err) {
        setError(err instanceof Error ? err.message : '레포지토리를 불러오는데 실패했습니다.');
      } finally {
        setIsLoading(false);
      }
    };

    loadRepositories();
  }, []);

  const handleToggle = (repo: GitHubRepository) => {
    const newSelected = new Set(selected);
    if (newSelected.has(repo.name)) {
      newSelected.delete(repo.name);
    } else {
      if (newSelected.size >= 8) {
        alert('최대 8개의 레포지토리만 선택할 수 있습니다.');
        return;
      }
      newSelected.add(repo.name);
    }
    setSelected(newSelected);
  };

  const handleConfirm = () => {
    const selectedRepos = repositories
      .filter((repo) => selected.has(repo.name))
      .map((repo) => ({
        name: repo.name,
        description: repo.description,
        html_url: repo.html_url,
        language: repo.language,
        stargazers_count: repo.stargazers_count,
        forks_count: repo.forks_count,
      }));
    onSelect(selectedRepos);
    onClose();
  };

  if (isLoading) {
    return (
      <div className={styles.overlay}>
        <div className={styles.modal}>
          <div className={styles.loading}>로딩 중...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.overlay}>
        <div className={styles.modal}>
          <div className={styles.error}>{error}</div>
          <button className={styles.closeButton} onClick={onClose}>
            닫기
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>
        <div className={styles.header}>
          <h3>레포지토리 선택 (최대 8개)</h3>
          <button className={styles.closeButton} onClick={onClose}>
            ×
          </button>
        </div>
        <div className={styles.content}>
          {repositories.map((repo) => (
            <div
              key={repo.name}
              className={`${styles.repoItem} ${selected.has(repo.name) ? styles.selected : ''}`}
              onClick={() => handleToggle(repo)}
            >
              <input
                type="checkbox"
                checked={selected.has(repo.name)}
                onChange={() => handleToggle(repo)}
                className={styles.checkbox}
              />
              <div className={styles.repoInfo}>
                <div className={styles.repoName}>{repo.name}</div>
                {repo.description && (
                  <div className={styles.repoDescription}>{repo.description}</div>
                )}
                <div className={styles.repoMeta}>
                  {repo.language && (
                    <span className={styles.language}>{repo.language}</span>
                  )}
                  <span className={styles.stars}>⭐ {repo.stargazers_count}</span>
                  <span className={styles.forks}>🍴 {repo.forks_count}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className={styles.footer}>
          <div className={styles.selectedCount}>
            선택됨: {selected.size} / 8
          </div>
          <button className={styles.confirmButton} onClick={handleConfirm}>
            확인
          </button>
        </div>
      </div>
    </div>
  );
};
