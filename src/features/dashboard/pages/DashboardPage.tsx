import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../auth/hooks/useAuth';
import { Button } from '../../../shared/components/Button';
import { fetchVisitorStats, recordVisit, VisitorStats } from '../api/dashboardApi';
import { hasVisitedToday, markVisitedToday } from '../../../shared/utils/storage';
import styles from './DashboardPage.module.css';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [stats, setStats] = useState<VisitorStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        setIsLoading(true);
        
        // 한국 시간 기준으로 오늘 이미 접속했는지 확인
        const alreadyVisited = hasVisitedToday();
        
        if (!alreadyVisited) {
          // 오늘 첫 접속인 경우에만 접속 기록
          try {
            const updatedStats = await recordVisit();
            setStats(updatedStats);
            markVisitedToday(); // 접속 기록 저장
          } catch (error) {
            console.error('Failed to record visit:', error);
            // 접속 기록 실패해도 통계만 조회
            const statsData = await fetchVisitorStats();
            setStats(statsData);
          }
        } else {
          // 이미 오늘 접속한 경우 통계만 조회
          const statsData = await fetchVisitorStats();
          setStats(statsData);
        }
      } catch (error) {
        console.error('Failed to load visitor stats:', error);
        // 실패해도 통계만 조회 시도
        try {
          const statsData = await fetchVisitorStats();
          setStats(statsData);
        } catch (fetchError) {
          console.error('Failed to fetch visitor stats:', fetchError);
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadStats();
  }, []);

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

        {/* 접속자 통계 */}
        {!isLoading && stats && (
          <div className={styles.statsContainer}>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{stats.today_visitors.toLocaleString()}</div>
              <div className={styles.statLabel}>오늘 접속자</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{stats.total_visitors.toLocaleString()}</div>
              <div className={styles.statLabel}>총 접속자</div>
            </div>
          </div>
        )}

        <div className={styles.buttonGroup}>
          <Button onClick={handleGoToBuilder} variant="primary">
            GitCard 시작하기
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

