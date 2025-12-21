export type StackBadge = {
  id: string;
  key: string;      // stackMeta의 스택 키 (예: "react", "fastapi")
  label: string;    // 표시 라벨 (재정의 가능, 기본값은 stackMeta 라벨)
  category: string; // 카테고리 (재정의 가능, 기본값은 stackMeta 카테고리)
  color: string;   // 배경 색상 (재정의 가능, 기본값은 stackMeta 색상)
};

export type ContactItem = {
  id: string;
  type?: string;    // contactMeta의 연락처 타입 (예: "mail", "instagram", "linkedin")
  label: string;    // 예: "Gmail", "Velog", "Notion" (재정의 가능)
  value: string;    // 예: 이메일 또는 URL
};

export type ProfileConfig = {
  cardTitle: string;     // 카드 목록에서 보이는 제목
  name: string;
  title: string;         // 프로필 카드에 표시되는 제목 (예: "AI & Full-stack Developer")
  tagline: string;       // 배너 아래 짧은 문장
  primaryColor: string;  // 그라데이션 시작 색상 (hex 색상)
  secondaryColor: string; // 그라데이션 끝 색상 (hex 색상)
  gradient: string;      // 배너에 사용할 그라데이션 문자열 (linear-gradient)
  showStacks: boolean;
  showContact: boolean;
  showGithubStats: boolean;
  // 백준 티어 (Solved.ac 배지)
  showBaekjoon: boolean;
  baekjoonId: string;
  // 기술 스택 카테고리 라벨 언어: 'ko' 또는 'en'
  stackLabelLang: 'ko' | 'en';
  stackAlignment: 'left' | 'center' | 'right';  // 스택 배지 정렬
  stacks: StackBadge[];
  contacts: ContactItem[];
};
