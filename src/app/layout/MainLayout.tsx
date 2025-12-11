import React, { useState } from 'react';
import { useAuth } from '../../features/auth/hooks/useAuth';
import { UserInfoModal } from '../../features/auth/components/UserInfoModal';
import styles from './MainLayout.module.css';

interface MainLayoutProps {
  children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const { user } = useAuth();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleAvatarClick = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.appName}>GitCard</h1>
        <div
          className={styles.avatar}
          onClick={handleAvatarClick}
          style={{
            cursor: 'pointer',
            backgroundImage: user?.avatar_url ? `url(${user.avatar_url})` : undefined,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        >
          {!user?.avatar_url && (
            <div className={styles.avatarPlaceholder}>
              {user?.name?.[0] || user?.github_login?.[0] || 'U'}
            </div>
          )}
        </div>
      </header>
      <main className={styles.main}>{children}</main>
      <UserInfoModal isOpen={isModalOpen} onClose={handleCloseModal} />
    </div>
  );
};
