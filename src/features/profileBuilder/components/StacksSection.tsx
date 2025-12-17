import React from 'react';
import { ProfileConfig } from '../types/profileConfig';
import { getStackMeta, type StackCategory } from '../../../shared/stackMeta';
import styles from './StacksSection.module.css';

interface StacksSectionProps {
  config: ProfileConfig;
}

// Category order matching stackMeta.ts
const categoryOrder: StackCategory[] = [
  "language", "frontend", "mobile", "backend", "database",
  "infra", "collaboration", "ai-ml", "testing", "tool"
];

// Category labels in Korean (matching stackMeta.ts structure)
const categoryLabels: Record<StackCategory, string> = {
  "language": "언어",
  "frontend": "프론트엔드",
  "mobile": "모바일",
  "backend": "백엔드",
  "database": "데이터베이스",
  "infra": "인프라",
  "collaboration": "협업 도구",
  "ai-ml": "AI/ML",
  "testing": "테스팅",
  "tool": "도구",
};

export const StacksSection: React.FC<StacksSectionProps> = ({ config }) => {
  if (!config.showStacks || config.stacks.length === 0) {
    return null;
  }

  // Organize stacks by category
  const stacksByCategory = config.stacks.reduce((acc, stack) => {
    const category = stack.category as StackCategory;
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(stack);
    return acc;
  }, {} as Record<StackCategory, typeof config.stacks>);

  return (
    <div className={styles.section}>
      <h2 className={styles.sectionTitle}>Stacks</h2>
      <div className={styles.content}>
        {/* Render categories in order matching stackMeta.ts */}
        {categoryOrder.map((category) => {
          const stacks = stacksByCategory[category];
          if (!stacks || stacks.length === 0) {
            return null;
          }

          const categoryLabel = categoryLabels[category] || category.toUpperCase();

          const alignmentStyle = {
            justifyContent: 
              config.stackAlignment === 'left' ? 'flex-start' :
              config.stackAlignment === 'right' ? 'flex-end' :
              'center'
          };

          return (
            <div key={category} className={styles.categoryGroup}>
              <h3 className={styles.categoryTitle}>{categoryLabel}</h3>
              <div className={styles.badges} style={alignmentStyle}>
                {stacks.map((stack) => {
                  // Use stackMeta if key exists, otherwise use stack's own values
                  const meta = stack.key ? getStackMeta(stack.key) : null;
                  const displayLabel = stack.label || meta?.label || stack.key || 'Unknown';
                  const displayColor = stack.color || meta?.color || '#667eea';
                  const iconSlug = meta?.icon;
                  
                  return (
                    <span
                      key={stack.id}
                      className={styles.badge}
                      style={{ backgroundColor: displayColor }}
                    >
                      {iconSlug && (
                        <img
                          src={`https://cdn.simpleicons.org/${iconSlug}/white`}
                          alt=""
                          className={styles.badgeIcon}
                        />
                      )}
                      {displayLabel}
                    </span>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

