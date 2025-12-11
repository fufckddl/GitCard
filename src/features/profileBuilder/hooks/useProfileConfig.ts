import { useState, useCallback } from 'react';
import { ProfileConfig, StackBadge, ContactItem } from '../types/profileConfig';

// 색상을 기반으로 그라데이션 생성 (GitHub stats 스타일과 유사하게)
const generateGradient = (color: string): string => {
  // hex 색상을 RGB로 변환
  const hex = color.replace('#', '');
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  
  // GitHub stats 스타일: 약간 더 어둡고 색조가 약간 다른 색상 생성
  // RGB 값을 조정하여 더 풍부한 그라데이션 효과
  const darkerR = Math.max(0, Math.min(255, Math.floor(r * 0.85 + 20)));
  const darkerG = Math.max(0, Math.min(255, Math.floor(g * 0.75 + 10)));
  const darkerB = Math.max(0, Math.min(255, Math.floor(b * 0.9 + 30)));
  
  const darkerColor = `rgb(${darkerR}, ${darkerG}, ${darkerB})`;
  
  // GitHub stats와 동일한 135deg 각도 사용
  return `linear-gradient(135deg, ${color} 0%, ${darkerColor} 100%)`;
};

const DEFAULT_PRIMARY_COLOR = '#667eea';

const DEFAULT_CONFIG: ProfileConfig = {
  cardTitle: '내 프로필 카드',
  name: 'James',
  title: 'AI & Full-stack Developer',
  tagline: 'Passionate about building amazing things',
  primaryColor: DEFAULT_PRIMARY_COLOR,
  gradient: generateGradient(DEFAULT_PRIMARY_COLOR),
  showStacks: true,
  showContact: true,
  showGithubStats: true,
  stacks: [
    { id: '1', key: 'react', label: 'React', category: 'frontend', color: '#61DAFB' },
    { id: '2', key: 'typescript', label: 'TypeScript', category: 'frontend', color: '#3178C6' },
    { id: '3', key: 'nodejs', label: 'Node.js', category: 'backend', color: '#339933' },
  ],
  contacts: [
    { id: '1', label: 'Gmail', value: 'example@gmail.com' },
    { id: '2', label: 'Velog', value: 'https://velog.io/@username' },
  ],
};

export const useProfileConfig = () => {
  const [config, setConfig] = useState<ProfileConfig>(DEFAULT_CONFIG);

  const updateConfig = useCallback((updates: Partial<ProfileConfig>) => {
    setConfig((prev) => {
      const newConfig = { ...prev, ...updates };
      // primaryColor가 변경되면 자동으로 gradient도 업데이트
      if (updates.primaryColor !== undefined) {
        newConfig.gradient = generateGradient(updates.primaryColor);
      }
      return newConfig;
    });
  }, []);

  const addStack = useCallback((stack: Omit<StackBadge, 'id'>) => {
    const newStack: StackBadge = {
      ...stack,
      id: Date.now().toString(),
    };
    setConfig((prev) => ({
      ...prev,
      stacks: [...prev.stacks, newStack],
    }));
  }, []);

  const updateStack = useCallback((id: string, updates: Partial<StackBadge>) => {
    setConfig((prev) => ({
      ...prev,
      stacks: prev.stacks.map((stack) =>
        stack.id === id ? { ...stack, ...updates } : stack
      ),
    }));
  }, []);

  const removeStack = useCallback((id: string) => {
    setConfig((prev) => ({
      ...prev,
      stacks: prev.stacks.filter((stack) => stack.id !== id),
    }));
  }, []);

  const addContact = useCallback((contact: Omit<ContactItem, 'id'>) => {
    const newContact: ContactItem = {
      ...contact,
      id: Date.now().toString(),
    };
    setConfig((prev) => ({
      ...prev,
      contacts: [...prev.contacts, newContact],
    }));
  }, []);

  const updateContact = useCallback((id: string, updates: Partial<ContactItem>) => {
    setConfig((prev) => ({
      ...prev,
      contacts: prev.contacts.map((contact) =>
        contact.id === id ? { ...contact, ...updates } : contact
      ),
    }));
  }, []);

  const removeContact = useCallback((id: string) => {
    setConfig((prev) => ({
      ...prev,
      contacts: prev.contacts.filter((contact) => contact.id !== id),
    }));
  }, []);

  return {
    config,
    updateConfig,
    addStack,
    updateStack,
    removeStack,
    addContact,
    updateContact,
    removeContact,
  };
};

