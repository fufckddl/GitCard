import React, { useState } from 'react';
import { useProfileConfig } from '../hooks/useProfileConfig';
import { StackBadgeEditor } from './StackBadgeEditor';
import { ContactEditor } from './ContactEditor';
import { StackSelector } from './StackSelector';
import { ContactSelector } from './ContactSelector';
import { getContactMeta, ContactMeta } from '../../../shared/contactMeta';
import styles from './BuilderSidebar.module.css';

interface BuilderSidebarProps {
  profileConfig: ReturnType<typeof useProfileConfig>;
}

export const BuilderSidebar: React.FC<BuilderSidebarProps> = ({ profileConfig }) => {
  const {
    config,
    updateConfig,
    addStack,
    updateStack,
    removeStack,
    addContact,
    updateContact,
    removeContact,
  } = profileConfig;

  const [activeTab, setActiveTab] = useState<'general' | 'stacks' | 'contacts'>('general');
  const [showStackSelector, setShowStackSelector] = useState(false);
  const [showContactSelector, setShowContactSelector] = useState(false);

  const handleAddStack = () => {
    setShowStackSelector(true);
  };

  const handleStackSelect = (stackMeta: { key: string; label: string; category: string; color: string }) => {
    addStack({
      key: stackMeta.key,
      label: stackMeta.label,
      category: stackMeta.category,
      color: stackMeta.color,
    });
    setShowStackSelector(false);
  };

  const handleAddContact = () => {
    setShowContactSelector(true);
  };

  const handleContactSelect = (contactMeta: ContactMeta) => {
    addContact({
      type: contactMeta.type,
      label: contactMeta.label,
      value: '',
    });
    setShowContactSelector(false);
  };

  return (
    <div className={styles.sidebar}>
      <div className={styles.tabs}>
        <button
          className={`${styles.tab} ${activeTab === 'general' ? styles.active : ''}`}
          onClick={() => setActiveTab('general')}
        >
          일반
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'stacks' ? styles.active : ''}`}
          onClick={() => setActiveTab('stacks')}
        >
          스택
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'contacts' ? styles.active : ''}`}
          onClick={() => setActiveTab('contacts')}
        >
          연락처
        </button>
      </div>

      <div className={styles.content}>
        {activeTab === 'general' && (
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>기본 정보</h3>
            <div className={styles.formGroup}>
              <label>이름</label>
              <input
                type="text"
                value={config.name}
                onChange={(e) => updateConfig({ name: e.target.value })}
                placeholder="Your name"
              />
            </div>
            <div className={styles.formGroup}>
              <label>프로필 제목 (카드 표시용)</label>
              <input
                type="text"
                value={config.title}
                onChange={(e) => updateConfig({ title: e.target.value })}
                placeholder="AI & Full-stack Developer"
              />
            </div>
            <div className={styles.formGroup}>
              <label>태그라인</label>
              <input
                type="text"
                value={config.tagline}
                onChange={(e) => updateConfig({ tagline: e.target.value })}
                placeholder="Short description"
              />
            </div>
            <div className={styles.formGroup}>
              <label>그라데이션 색상 1</label>
              <div className={styles.colorPickerContainer}>
                <input
                  type="color"
                  value={config.primaryColor}
                  onChange={(e) => updateConfig({ primaryColor: e.target.value })}
                  className={styles.colorPicker}
                />
                <input
                  type="text"
                  value={config.primaryColor}
                  onChange={(e) => updateConfig({ primaryColor: e.target.value })}
                  className={styles.colorInput}
                  placeholder="#667eea"
                  pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
                />
              </div>
            </div>
            <div className={styles.formGroup}>
              <label>그라데이션 색상 2</label>
              <div className={styles.colorPickerContainer}>
                <input
                  type="color"
                  value={config.secondaryColor}
                  onChange={(e) => updateConfig({ secondaryColor: e.target.value })}
                  className={styles.colorPicker}
                />
                <input
                  type="text"
                  value={config.secondaryColor}
                  onChange={(e) => updateConfig({ secondaryColor: e.target.value })}
                  className={styles.colorInput}
                  placeholder="#764ba2"
                  pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
                />
              </div>
            </div>
            <div className={styles.formGroup}>
              <label className={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={config.showStacks}
                  onChange={(e) => updateConfig({ showStacks: e.target.checked })}
                />
                스택 섹션 표시
              </label>
            </div>
            {config.showStacks && (
              <div className={styles.formGroup}>
                <label>스택 배지 정렬</label>
                <select
                  value={config.stackAlignment}
                  onChange={(e) => updateConfig({ stackAlignment: e.target.value as 'left' | 'center' | 'right' })}
                  className={styles.select}
                >
                  <option value="left">좌측</option>
                  <option value="center">가운데</option>
                  <option value="right">우측</option>
                </select>
              </div>
            )}
            <div className={styles.formGroup}>
              <label className={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={config.showContact}
                  onChange={(e) => updateConfig({ showContact: e.target.checked })}
                />
                연락처 섹션 표시
              </label>
            </div>
            <div className={styles.formGroup}>
              <label className={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={config.showGithubStats}
                  onChange={(e) => updateConfig({ showGithubStats: e.target.checked })}
                />
                GitHub 통계 표시
              </label>
            </div>
          </div>
        )}

        {activeTab === 'stacks' && (
          <div className={styles.section}>
            <div className={styles.sectionHeader}>
              <h3 className={styles.sectionTitle}>스택 배지</h3>
              <button className={styles.addButton} onClick={handleAddStack}>
                + 추가
              </button>
            </div>
            {showStackSelector && (
              <StackSelector
                onSelect={handleStackSelect}
                onClose={() => setShowStackSelector(false)}
              />
            )}
            <div className={styles.list}>
              {config.stacks.map((stack) => (
                <StackBadgeEditor
                  key={stack.id}
                  stack={stack}
                  onUpdate={(updates) => updateStack(stack.id, updates)}
                  onDelete={() => removeStack(stack.id)}
                />
              ))}
              {config.stacks.length === 0 && (
                <div className={styles.emptyState}>
                  스택이 없습니다. 추가 버튼을 클릭하세요.
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'contacts' && (
          <div className={styles.section}>
            <div className={styles.sectionHeader}>
              <h3 className={styles.sectionTitle}>연락처</h3>
              <button className={styles.addButton} onClick={handleAddContact}>
                + 추가
              </button>
            </div>
            {showContactSelector && (
              <ContactSelector
                onSelect={handleContactSelect}
                onClose={() => setShowContactSelector(false)}
              />
            )}
            <div className={styles.list}>
              {config.contacts.map((contact) => (
                <ContactEditor
                  key={contact.id}
                  contact={contact}
                  onUpdate={(updates) => updateContact(contact.id, updates)}
                  onDelete={() => removeContact(contact.id)}
                />
              ))}
              {config.contacts.length === 0 && (
                <div className={styles.emptyState}>
                  연락처가 없습니다. 추가 버튼을 클릭하세요.
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

