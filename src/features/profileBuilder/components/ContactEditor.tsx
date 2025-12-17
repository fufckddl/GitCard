import React, { useState } from 'react';
import { ContactItem } from '../types/profileConfig';
import { getContactMeta } from '../../../shared/contactMeta';
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
  const contactMeta = contact.type ? getContactMeta(contact.type as any) : null;
  const displayLabel = contact.label || contactMeta?.label || 'Contact';
  const displayIcon = contactMeta?.icon;

  return (
    <div className={styles.container}>
      <div className={styles.header} onClick={() => setIsExpanded(!isExpanded)}>
        <div className={styles.preview}>
          {displayIcon && (
            <img
              src={`https://cdn.simpleicons.org/${displayIcon}/white`}
              alt={displayLabel}
              className={styles.icon}
            />
          )}
          <span className={styles.label}>{displayLabel}</span>
          <span className={styles.value}>{contact.value}</span>
          {contact.type && (
            <span className={styles.type}>{contact.type}</span>
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
            <label>Type</label>
            <input
              type="text"
              value={contact.type || ''}
              onChange={(e) => onUpdate({ type: e.target.value })}
              placeholder="e.g. mail, instagram, linkedin"
            />
            <small className={styles.helpText}>
              타입: mail, instagram, linkedin, velog, reddit, facebook, youtube
            </small>
          </div>
          <div className={styles.formGroup}>
            <label>Label</label>
            <input
              type="text"
              value={contact.label}
              onChange={(e) => onUpdate({ label: e.target.value })}
              placeholder={contactMeta?.placeholder || "e.g. Gmail, Velog, Notion"}
            />
          </div>
          <div className={styles.formGroup}>
            <label>Value</label>
            <input
              type="text"
              value={contact.value}
              onChange={(e) => onUpdate({ value: e.target.value })}
              placeholder={contactMeta?.placeholder || "e.g. email@example.com or https://..."}
            />
          </div>
        </div>
      )}
    </div>
  );
};

