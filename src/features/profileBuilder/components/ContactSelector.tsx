import React, { useState, useMemo } from 'react';
import {
  getAllContactTypes,
  getContactMeta,
  ContactMeta,
} from '../../../shared/contactMeta';
import styles from './ContactSelector.module.css';

interface ContactSelectorProps {
  onSelect: (contactMeta: ContactMeta) => void;
  onClose: () => void;
}

export const ContactSelector: React.FC<ContactSelectorProps> = ({ onSelect, onClose }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const contactTypes = getAllContactTypes();

  // Filter contacts based on search
  const filteredContacts = useMemo(() => {
    let contacts: ContactMeta[] = contactTypes
      .map((type) => getContactMeta(type)!)
      .filter(Boolean);

    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      contacts = contacts.filter(
        (contact) =>
          contact.type.toLowerCase().includes(query) ||
          contact.label.toLowerCase().includes(query)
      );
    }

    return contacts;
  }, [searchQuery]);

  const handleContactClick = (contactMeta: ContactMeta) => {
    onSelect(contactMeta);
    onClose();
  };

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h3 className={styles.title}>연락처 타입 선택</h3>
          <button className={styles.closeButton} onClick={onClose}>
            ✕
          </button>
        </div>
        <div className={styles.searchContainer}>
          <input
            type="text"
            className={styles.searchInput}
            placeholder="검색..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            autoFocus
          />
        </div>
        <div className={styles.list}>
          {filteredContacts.map((contactMeta) => (
            <div
              key={contactMeta.type}
              className={styles.item}
              onClick={() => handleContactClick(contactMeta)}
            >
              <div className={styles.iconContainer}>
                <img
                  src={`https://cdn.simpleicons.org/${contactMeta.icon}/white`}
                  alt={contactMeta.label}
                  className={styles.icon}
                />
              </div>
              <div className={styles.info}>
                <span className={styles.label}>{contactMeta.label}</span>
                <span className={styles.type}>{contactMeta.type}</span>
              </div>
            </div>
          ))}
          {filteredContacts.length === 0 && (
            <div className={styles.emptyState}>검색 결과가 없습니다.</div>
          )}
        </div>
      </div>
    </div>
  );
};
