/**
 * Contact Type System for GitHub Profile README Builder
 * 
 * Similar to stackMeta.ts, but for contact types
 */

export type ContactType =
  | "mail"
  | "instagram"
  | "linkedin"
  | "velog"
  | "reddit"
  | "facebook"
  | "youtube"
  | "x"
  | "thread";

export interface ContactMeta {
  type: ContactType;
  label: string;
  icon: string; // Simple Icons slug
  color: string; // hex color for badges
  placeholder: string; // placeholder text for value input
}

/**
 * Main array of all contact metadata entries.
 */
export const CONTACT_META_LIST: ContactMeta[] = [
  {
    type: "mail",
    label: "Email",
    icon: "gmail",
    color: "#EA4335",
    placeholder: "example@gmail.com",
  },
  {
    type: "instagram",
    label: "Instagram",
    icon: "instagram",
    color: "#E4405F",
    placeholder: "https://instagram.com/username",
  },
  {
    type: "linkedin",
    label: "LinkedIn",
    icon: "inspire",
    color: "#0077B5",
    placeholder: "https://linkedin.com/in/username",
  },
  {
    type: "velog",
    label: "Velog",
    icon: "velog",
    color: "#20C997",
    placeholder: "https://velog.io/@username",
  },
  {
    type: "reddit",
    label: "Reddit",
    icon: "reddit",
    color: "#FF4500",
    placeholder: "https://reddit.com/user/username",
  },
  {
    type: "facebook",
    label: "Facebook",
    icon: "facebook",
    color: "#1877F2",
    placeholder: "https://facebook.com/username",
  },
  {
    type: "youtube",
    label: "YouTube",
    icon: "youtube",
    color: "#FF0000",
    placeholder: "https://youtube.com/@username",
  },
  {
    type: "x",
    label: "X (Twitter)",
    icon: "x",
    color: "#000000",
    placeholder: "https://x.com/username",
  },
  {
    type: "thread",
    label: "Threads",
    icon: "threads",
    color: "#000000",
    placeholder: "https://threads.net/@username",
  },
];

/**
 * Fast lookup map: contact type → ContactMeta
 */
export const CONTACT_META_MAP: ReadonlyMap<ContactType, ContactMeta> = new Map(
  CONTACT_META_LIST.map((meta) => [meta.type, meta])
);

/**
 * Get contact metadata by type.
 */
export function getContactMeta(type: ContactType): ContactMeta | undefined {
  return CONTACT_META_MAP.get(type);
}

/**
 * Get all available contact types.
 */
export function getAllContactTypes(): ContactType[] {
  return CONTACT_META_LIST.map((meta) => meta.type);
}
