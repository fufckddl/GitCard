import { useState, useEffect } from 'react';
import { getToken, setToken as saveToken, clearToken } from '../../../shared/utils/storage';
import { fetchCurrentUser } from '../api/userApi';
import { User } from '../types';

interface UseAuthReturn {
  token: string | null;
  user: User | null;
  login: (token: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
  refreshUser: () => Promise<void>;
}

export const useAuth = (): UseAuthReturn => {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedToken = getToken();
    setToken(storedToken);
    
    if (storedToken) {
      loadUser(storedToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  const loadUser = async (authToken: string) => {
    try {
      setIsLoading(true);
      const userData = await fetchCurrentUser(authToken);
      setUser(userData);
    } catch (error) {
      console.error('Failed to load user:', error);
      // Token might be invalid, clear it
      clearToken();
      setToken(null);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = (newToken: string) => {
    saveToken(newToken);
    setToken(newToken);
    loadUser(newToken);
  };

  const logout = () => {
    clearToken();
    setToken(null);
    setUser(null);
  };

  const refreshUser = async () => {
    const currentToken = getToken();
    if (currentToken) {
      await loadUser(currentToken);
    }
  };

  return {
    token,
    user,
    login,
    logout,
    isAuthenticated: !!token && !!user,
    isLoading,
    refreshUser,
  };
};
