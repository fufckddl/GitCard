import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../../../shared/components/Button';
import styles from './UserInfoModal.module.css';

interface UserInfoModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const UserInfoModal: React.FC<UserInfoModalProps> = ({ isOpen, onClose }) => {
  const { user, logout } = useAuth();

  if (!isOpen || !user) return null;

  const handleLogout = () => {
    logout();
    onClose();
    window.location.href = '/login';
  };

  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className={styles.overlay} onClick={handleOverlayClick}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h2 className={styles.title}>사용자 정보</h2>
          <button className={styles.closeButton} onClick={onClose}>
            ×
          </button>
        </div>

        <div className={styles.content}>
          {user.avatar_url && (
            <div className={styles.avatarContainer}>
              <img
                src={user.avatar_url}
                alt={user.name || user.github_login}
                className={styles.avatarImage}
              />
            </div>
          )}

          <div className={styles.infoSection}>
            <div className={styles.infoRow}>
              <span className={styles.label}>이름:</span>
              <span className={styles.value}>{user.name || 'N/A'}</span>
            </div>

            <div className={styles.infoRow}>
              <span className={styles.label}>GitHub 사용자명:</span>
              <span className={styles.value}>
                {user.html_url ? (
                  <a
                    href={user.html_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={styles.link}
                  >
                    {user.github_login}
                  </a>
                ) : (
                  user.github_login
                )}
              </span>
            </div>

            <div className={styles.infoRow}>
              <span className={styles.label}>이메일:</span>
              <span className={styles.value}>
                {user.email ? (
                  <a href={`mailto:${user.email}`} className={styles.link}>
                    {user.email}
                  </a>
                ) : (
                  'N/A'
                )}
              </span>
            </div>

            <div className={styles.infoRow}>
              <span className={styles.label}>GitHub ID:</span>
              <span className={styles.value}>{user.github_id}</span>
            </div>

            {user.created_at && (
              <div className={styles.infoRow}>
                <span className={styles.label}>가입일:</span>
                <span className={styles.value}>
                  {new Date(user.created_at).toLocaleDateString('ko-KR')}
                </span>
              </div>
            )}
          </div>
        </div>

        <div className={styles.footer}>
          <Button onClick={handleLogout} variant="secondary">
            로그아웃
          </Button>
        </div>
      </div>
    </div>
  );
};

