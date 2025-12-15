export type StackBadge = {
  id: string;
  key: string;      // Stack key from stackMeta (e.g., "react", "fastapi")
  label: string;    // Display label (can be overridden, but defaults to stackMeta label)
  category: string; // Category (can be overridden, but defaults to stackMeta category)
  color: string;   // Background color (can be overridden, but defaults to stackMeta color)
};

export type ContactItem = {
  id: string;
  label: string;    // e.g. "Gmail", "Velog", "Notion"
  value: string;    // e.g. email or URL
};

export type ProfileConfig = {
  cardTitle: string;     // 카드 목록에서 보이는 제목
  name: string;
  title: string;         // 프로필 카드에 표시되는 제목 (e.g. "AI & Full-stack Developer")
  tagline: string;       // short sentence under banner
  primaryColor: string;  // 그라데이션 시작 색상 (hex color)
  secondaryColor: string; // 그라데이션 끝 색상 (hex color)
  gradient: string;      // 배너에 사용할 그라데이션 문자열 (linear-gradient)
  showStacks: boolean;
  showContact: boolean;
  showGithubStats: boolean;
  stacks: StackBadge[];
  contacts: ContactItem[];
};

