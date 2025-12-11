import React, { useState, useMemo } from 'react';
import {
  getStacksByCategory,
  getAllCategories,
  StackCategory,
  StackMeta,
} from '../../../shared/stackMeta';
import styles from './StackSelector.module.css';

interface StackSelectorProps {
  onSelect: (stackMeta: StackMeta) => void;
  onClose: () => void;
}

export const StackSelector: React.FC<StackSelectorProps> = ({ onSelect, onClose }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<StackCategory | 'all'>('all');
  const categories = getAllCategories();

  // Filter stacks based on search and category
  const filteredStacks = useMemo(() => {
    let stacks: StackMeta[] = [];

    if (selectedCategory === 'all') {
      stacks = getAllCategories().flatMap((cat) => getStacksByCategory(cat));
    } else {
      stacks = getStacksByCategory(selectedCategory);
    }

    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      stacks = stacks.filter(
        (stack) =>
          stack.key.toLowerCase().includes(query) ||
          stack.label.toLowerCase().includes(query)
      );
    }

    return stacks;
  }, [searchQuery, selectedCategory]);

  const handleStackClick = (stackMeta: StackMeta) => {
    onSelect(stackMeta);
    onClose();
  };

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h3 className={styles.title}>스택 선택</h3>
          <button className={styles.closeButton} onClick={onClose}>
            ×
          </button>
        </div>

        <div className={styles.searchContainer}>
          <input
            type="text"
            className={styles.searchInput}
            placeholder="스택 검색 (예: react, python, docker...)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            autoFocus
          />
        </div>

        <div className={styles.content}>
          <div className={styles.categoryFilter}>
            <button
              className={`${styles.categoryButton} ${selectedCategory === 'all' ? styles.active : ''}`}
              onClick={() => setSelectedCategory('all')}
            >
              전체
            </button>
            {categories.map((category) => (
              <button
                key={category}
                className={`${styles.categoryButton} ${selectedCategory === category ? styles.active : ''}`}
                onClick={() => setSelectedCategory(category)}
              >
                {getCategoryLabel(category)}
              </button>
            ))}
          </div>

          <div className={styles.stackList}>
            {filteredStacks.length === 0 ? (
              <div className={styles.emptyState}>
                검색 결과가 없습니다.
              </div>
            ) : (
              filteredStacks.map((stack) => (
                <button
                  key={stack.key}
                  className={styles.stackItem}
                  onClick={() => handleStackClick(stack)}
                >
                  <span
                    className={styles.stackBadge}
                    style={{ backgroundColor: stack.color }}
                  >
                    {stack.label}
                  </span>
                  <span className={styles.stackKey}>{stack.key}</span>
                </button>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

function getCategoryLabel(category: StackCategory): string {
  const labels: Record<StackCategory, string> = {
    language: '언어',
    frontend: '프론트엔드',
    mobile: '모바일',
    backend: '백엔드',
    database: '데이터베이스',
    infra: '인프라/DevOps',
    collaboration: '협업 도구',
    'ai-ml': 'AI/ML',
    testing: '테스팅',
    tool: '도구',
  };
  return labels[category] || category;
}




