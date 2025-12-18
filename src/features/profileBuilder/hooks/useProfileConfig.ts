import { useState, useCallback } from 'react';
import { ProfileConfig, StackBadge, ContactItem } from '../types/profileConfig';

// 두 색상을 기반으로 그라데이션 생성
const generateGradient = (startColor: string, endColor: string): string => {
  // GitHub stats와 동일한 135deg 각도 사용
  return `linear-gradient(135deg, ${startColor} 0%, ${endColor} 100%)`;
};

const DEFAULT_PRIMARY_COLOR = '#667eea';
const DEFAULT_SECONDARY_COLOR = '#764ba2';

const DEFAULT_CONFIG: ProfileConfig = {
  cardTitle: '내 프로필 카드',
  name: 'James',
  title: 'AI & Full-stack Developer',
  tagline: 'Passionate about building amazing things',
  primaryColor: DEFAULT_PRIMARY_COLOR,
  secondaryColor: DEFAULT_SECONDARY_COLOR,
  gradient: generateGradient(DEFAULT_PRIMARY_COLOR, DEFAULT_SECONDARY_COLOR),
  showStacks: true,
  showContact: true,
  showGithubStats: true,
  showBaekjoon: false,
  baekjoonId: '',
  stackAlignment: 'center',
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
      // primaryColor 또는 secondaryColor가 변경되면 자동으로 gradient도 업데이트
      if (updates.primaryColor !== undefined || updates.secondaryColor !== undefined) {
        const start = newConfig.primaryColor || DEFAULT_PRIMARY_COLOR;
        const end = newConfig.secondaryColor || DEFAULT_SECONDARY_COLOR;
        newConfig.gradient = generateGradient(start, end);
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
