import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../auth/hooks/useAuth';
import { Button } from '../../../shared/components/Button';
import styles from './DashboardPage.module.css';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleGoToBuilder = () => {
    navigate('/builder');
  };

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <h1 className={styles.title}>GitCard</h1>
        <p className={styles.message}>
          로그인 완료! GitCard 대시보드를 준비 중입니다.
        </p>
        <div className={styles.buttonGroup}>
          <Button onClick={handleGoToBuilder} variant="primary">
            프로필 빌더 시작하기
          </Button>
          <Button onClick={() => navigate('/dashboard/cards')} variant="secondary">
            내 카드 목록
          </Button>
          <Button onClick={handleLogout} variant="secondary">
            로그아웃
          </Button>
        </div>
      </div>
    </div>
  );
};

