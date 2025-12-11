import React, { useState, useEffect } from 'react';
import { StackBadge } from '../types/profileConfig';
import { getStackMeta } from '../../../shared/stackMeta';
import styles from './StackBadgeEditor.module.css';

interface StackBadgeEditorProps {
  stack: StackBadge;
  onUpdate: (updates: Partial<StackBadge>) => void;
  onDelete: () => void;
}

export const StackBadgeEditor: React.FC<StackBadgeEditorProps> = ({
  stack,
  onUpdate,
  onDelete,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  // Get metadata from stackMeta if key exists
  const stackMeta = stack.key ? getStackMeta(stack.key) : null;
  
  // Use metadata values as defaults, but allow overrides
  const displayLabel = stack.label || stackMeta?.label || stack.key || 'Unknown';
  const displayCategory = stack.category || stackMeta?.category || '';
  const displayColor = stack.color || stackMeta?.color || '#667eea';
  
  // Sync with stackMeta when key changes
  useEffect(() => {
    if (stack.key && stackMeta) {
      // Auto-update if using default values
      if (!stack.label || stack.label === 'New Stack') {
        onUpdate({ label: stackMeta.label });
      }
      if (!stack.category || stack.category === 'Frontend') {
        onUpdate({ category: stackMeta.category });
      }
      if (!stack.color || stack.color === '#667eea') {
        onUpdate({ color: stackMeta.color });
      }
    }
  }, [stack.key, stackMeta, onUpdate]);

  return (
    <div className={styles.container}>
      <div className={styles.header} onClick={() => setIsExpanded(!isExpanded)}>
        <div className={styles.preview}>
          <span
            className={styles.badgePreview}
            style={{ backgroundColor: displayColor }}
          >
            {displayLabel}
          </span>
          <span className={styles.category}>{displayCategory}</span>
          {stack.key && (
            <span className={styles.stackKey}>{stack.key}</span>
          )}
        </div>
        <div className={styles.actions}>
          <button
            className={styles.toggleButton}
            onClick={(e) => {
              e.stopPropagation();
              setIsExpanded(!isExpanded);
            }}
          >
            {isExpanded ? '▼' : '▶'}
          </button>
          <button className={styles.deleteButton} onClick={onDelete}>
            삭제
          </button>
        </div>
      </div>
      {isExpanded && (
        <div className={styles.form}>
          <div className={styles.formGroup}>
            <label>Stack Key</label>
            <input
              type="text"
              value={stack.key || ''}
              onChange={(e) => {
                const newKey = e.target.value;
                const meta = newKey ? getStackMeta(newKey) : null;
                onUpdate({
                  key: newKey,
                  ...(meta ? {
                    label: meta.label,
                    category: meta.category,
                    color: meta.color,
                  } : {}),
                });
              }}
              placeholder="e.g. react, fastapi, docker"
            />
            {stack.key && stackMeta && (
              <span className={styles.metaHint}>✓ stackMeta에서 자동 로드됨</span>
            )}
            {stack.key && !stackMeta && (
              <span className={styles.metaWarning}>⚠ 알 수 없는 키 (수동 입력 필요)</span>
            )}
          </div>
          <div className={styles.formGroup}>
            <label>Label (표시 이름)</label>
            <input
              type="text"
              value={stack.label}
              onChange={(e) => onUpdate({ label: e.target.value })}
              placeholder={stackMeta?.label || "e.g. React"}
            />
          </div>
          <div className={styles.formGroup}>
            <label>Category</label>
            <input
              type="text"
              value={stack.category}
              onChange={(e) => onUpdate({ category: e.target.value })}
              placeholder={stackMeta?.category || "e.g. frontend"}
            />
          </div>
          <div className={styles.formGroup}>
            <label>Color</label>
            <div className={styles.colorInput}>
              <input
                type="color"
                value={stack.color}
                onChange={(e) => onUpdate({ color: e.target.value })}
              />
              <input
                type="text"
                value={stack.color}
                onChange={(e) => onUpdate({ color: e.target.value })}
                placeholder={stackMeta?.color || "#61DAFB"}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

