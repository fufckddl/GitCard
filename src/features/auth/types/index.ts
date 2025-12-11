export type AuthToken = string;

export interface User {
  id: number;
  github_id: number;
  github_login: string;
  name: string | null;
  email: string | null;
  avatar_url: string | null;
  html_url: string | null;
  created_at: string | null;
  last_login_at: string | null;
}
