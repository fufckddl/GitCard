import React, { useState } from 'react';
import { ContactItem } from '../types/profileConfig';
import styles from './ContactEditor.module.css';

interface ContactEditorProps {
  contact: ContactItem;
  onUpdate: (updates: Partial<ContactItem>) => void;
  onDelete: () => void;
}

export const ContactEditor: React.FC<ContactEditorProps> = ({
  contact,
  onUpdate,
  onDelete,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={styles.container}>
      <div className={styles.header} onClick={() => setIsExpanded(!isExpanded)}>
        <div className={styles.preview}>
          <span className={styles.label}>{contact.label}</span>
          <span className={styles.value}>{contact.value}</span>
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
            <label>Label</label>
            <input
              type="text"
              value={contact.label}
              onChange={(e) => onUpdate({ label: e.target.value })}
              placeholder="e.g. Gmail, Velog, Notion"
            />
          </div>
          <div className={styles.formGroup}>
            <label>Value</label>
            <input
              type="text"
              value={contact.value}
              onChange={(e) => onUpdate({ value: e.target.value })}
              placeholder="e.g. email@example.com or https://..."
            />
          </div>
        </div>
      )}
    </div>
  );
};

