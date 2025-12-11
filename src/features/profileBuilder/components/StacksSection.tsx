import React from 'react';
import { ProfileConfig } from '../types/profileConfig';
import { getStackMeta } from '../../../shared/stackMeta';
import styles from './StacksSection.module.css';

interface StacksSectionProps {
  config: ProfileConfig;
}

export const StacksSection: React.FC<StacksSectionProps> = ({ config }) => {
  if (!config.showStacks || config.stacks.length === 0) {
    return null;
  }

  const stacksByCategory = config.stacks.reduce((acc, stack) => {
    if (!acc[stack.category]) {
      acc[stack.category] = [];
    }
    acc[stack.category].push(stack);
    return acc;
  }, {} as Record<string, typeof config.stacks>);

  return (
    <div className={styles.section}>
      <h2 className={styles.sectionTitle}>Stacks</h2>
      <div className={styles.content}>
        {Object.entries(stacksByCategory).map(([category, stacks]) => (
          <div key={category} className={styles.categoryGroup}>
            <h3 className={styles.categoryTitle}>{category}</h3>
            <div className={styles.badges}>
              {stacks.map((stack) => {
                // Use stackMeta if key exists, otherwise use stack's own values
                const meta = stack.key ? getStackMeta(stack.key) : null;
                const displayLabel = stack.label || meta?.label || stack.key || 'Unknown';
                const displayColor = stack.color || meta?.color || '#667eea';
                
                return (
                  <span
                    key={stack.id}
                    className={styles.badge}
                    style={{ backgroundColor: displayColor }}
                  >
                    {displayLabel}
                  </span>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

