import React from 'react';
import { ProfileConfig } from '../types/profileConfig';
import styles from './ContactSection.module.css';

interface ContactSectionProps {
  config: ProfileConfig;
}

export const ContactSection: React.FC<ContactSectionProps> = ({ config }) => {
  if (!config.showContact || config.contacts.length === 0) {
    return null;
  }

  const isEmail = (value: string) => value.includes('@');
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

          return (
            <a
              key={contact.id}
              href={href}
              target={isUrl(contact.value) || !isEmail(contact.value) ? '_blank' : undefined}
              rel={isUrl(contact.value) || !isEmail(contact.value) ? 'noopener noreferrer' : undefined}
              className={styles.contactCard}
            >
              <span className={styles.label}>{contact.label}</span>
              <span className={styles.value}>{contact.value}</span>
            </a>
          );
        })}
      </div>
    </div>
  );
};

