import React from 'react';
import { ProfileConfig } from '../types/profileConfig';
import { getContactMeta } from '../../../shared/contactMeta';
import styles from './ContactSection.module.css';

interface ContactSectionProps {
  config: ProfileConfig;
}

export const ContactSection: React.FC<ContactSectionProps> = ({ config }) => {
  if (!config.showContact || config.contacts.length === 0) {
    return null;
  }

  const isEmail = (value: string) => value.includes('@') && !value.startsWith('http');
  const isUrl = (value: string) => value.startsWith('http://') || value.startsWith('https://');

  return (
    <div className={styles.section}>
      <h2 className={styles.sectionTitle}>Contact</h2>
      <div className={styles.content}>
        {config.contacts.map((contact) => {
          let href = contact.value;
          if (isEmail(contact.value)) {
            href = `mailto:${contact.value}`;
          } else if (!isUrl(contact.value)) {
            href = `https://${contact.value}`;
          }

          const contactMeta = contact.type ? getContactMeta(contact.type as any) : null;
          const displayLabel = contact.label || contactMeta?.label || 'Contact';
          const displayIcon = contactMeta?.icon;

          return (
            <a
              key={contact.id}
              href={href}
              target={isUrl(contact.value) || !isEmail(contact.value) ? '_blank' : undefined}
              rel={isUrl(contact.value) || !isEmail(contact.value) ? 'noopener noreferrer' : undefined}
              className={styles.contactCard}
            >
              {displayIcon && (
                <img
                  src={`https://cdn.simpleicons.org/${displayIcon}/white`}
                  alt={displayLabel}
                  className={styles.icon}
                />
              )}
              <div className={styles.textContainer}>
                <span className={styles.label}>{displayLabel}</span>
                <span className={styles.value}>{contact.value}</span>
              </div>
            </a>
          );
        })}
      </div>
    </div>
  );
};

