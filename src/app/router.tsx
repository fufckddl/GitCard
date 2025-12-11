import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from '../features/auth/pages/LoginPage';
import { AuthCallbackPage } from '../features/auth/pages/AuthCallbackPage';
import { DashboardPage } from '../features/dashboard/pages/DashboardPage';
import { ProfileBuilderPage } from '../features/profileBuilder/pages/ProfileBuilderPage';
import { ProfileCardListPage } from '../features/profileBuilder/pages/ProfileCardListPage';
import { ProfileCardDetailPage } from '../features/profileBuilder/pages/ProfileCardDetailPage';
import { PublicProfileCardPage } from '../features/profileBuilder/pages/PublicProfileCardPage';
import { MainLayout } from './layout/MainLayout';
import { RequireAuth } from './RequireAuth';

export const AppRouter: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/auth/callback" element={<AuthCallbackPage />} />
      <Route
        path="/dashboard"
        element={
          <RequireAuth>
            <MainLayout>
              <DashboardPage />
            </MainLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/builder"
        element={
          <RequireAuth>
            <MainLayout>
              <ProfileBuilderPage />
            </MainLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/dashboard/cards"
        element={
          <RequireAuth>
            <MainLayout>
              <ProfileCardListPage />
            </MainLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/dashboard/cards/:cardId"
        element={
          <RequireAuth>
            <MainLayout>
              <ProfileCardDetailPage />
            </MainLayout>
          </RequireAuth>
        }
      />
      {/* Public profile card page (no authentication required) */}
      <Route
        path="/dashboard/:githubLogin/cards/:cardId"
        element={<PublicProfileCardPage />}
      />
      <Route path="/" element={<RootRedirect />} />
    </Routes>
  );
};

const RootRedirect: React.FC = () => {
  const token = localStorage.getItem('auth_token');
  return <Navigate to={token ? '/dashboard' : '/login'} replace />;
};

