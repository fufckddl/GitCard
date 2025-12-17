/**
 * Stack Tag System for GitHub Profile README Builder
 * 
 * ============================================================================
 * DESIGN GUIDELINES
 * ============================================================================
 * 
 * 1. KEY NAMING RULE
 *    - All lowercase
 *    - Words separated by hyphens (`-`)
 *    - No spaces
 *    - Examples: `react`, `react-native`, `spring-boot`, `yolov8`, `github-actions`
 * 
 * 2. STACK CATEGORY RULE
 *    - Each tag must belong to exactly one category
 *    - Categories: "language" | "frontend" | "mobile" | "backend" | "database" 
 *                  | "infra" | "collaboration" | "ai-ml" | "testing" | "tool"
 * 
 * 3. SEPARATION OF CONCERNS
 *    - Components should only store **keys** (e.g., `"react"`, `"fastapi"`)
 *    - Styling (color, label, icon mapping) must be centralized in this file
 *    - No other file should hard-code labels/colors
 * 
 * 4. EXTENSIBILITY GUIDELINE
 *    To add a new tag:
 *    1) Pick a `key` following the naming rule
 *    2) Choose the right `category`
 *    3) Add a `label` (human readable)
 *    4) Choose a `color` (hex string)
 * 
 * 5. USAGE PATTERN
 *    - UI components can:
 *      - Receive `string[]` of stack keys from user profile data
 *      - Call `getStackMeta(key)` to render name/color
 *      - Group by `StackCategory` using `getStacksByCategory` or `STACKS_BY_CATEGORY`
 * 
 * ============================================================================
 */

export type StackCategory =
  | "language"
  | "frontend"
  | "mobile"
  | "backend"
  | "database"
  | "infra"
  | "collaboration"
  | "ai-ml"
  | "testing"
  | "tool";

export interface StackMeta {
  key: string;
  label: string;
  category: StackCategory;
  color: string; // hex color
  icon?: string; // Simple Icons slug (e.g., "javascript", "react", "python")
}

/**
 * Main array of all stack metadata entries.
 * Add new stacks here following the design guidelines above.
 */
export const STACK_META_LIST: StackMeta[] = [
  // ==========================================================================
  // LANGUAGES
  // ==========================================================================
  { key: "javascript", label: "JavaScript", category: "language", color: "#F7DF1E", icon: "javascript" },
  { key: "typescript", label: "TypeScript", category: "language", color: "#3178C6", icon: "typescript" },
  { key: "python", label: "Python", category: "language", color: "#3776AB", icon: "python" },
  { key: "java", label: "Java", category: "language", color: "#ED8B00", icon: "java" },
  { key: "kotlin", label: "Kotlin", category: "language", color: "#7F52FF", icon: "kotlin" },
  { key: "swift", label: "Swift", category: "language", color: "#FA7343", icon: "swift" },
  { key: "dart", label: "Dart", category: "language", color: "#0175C2", icon: "dart" },
  { key: "c", label: "C", category: "language", color: "#A8B9CC", icon: "c" },
  { key: "cpp", label: "C++", category: "language", color: "#00599C", icon: "cplusplus" },
  { key: "csharp", label: "C#", category: "language", color: "#239120", icon: "csharp" },
  { key: "go", label: "Go", category: "language", color: "#00ADD8", icon: "go" },
  { key: "rust", label: "Rust", category: "language", color: "#000000", icon: "rust" },
  { key: "php", label: "PHP", category: "language", color: "#777BB4", icon: "php" },
  { key: "ruby", label: "Ruby", category: "language", color: "#CC342D", icon: "ruby" },
  { key: "scala", label: "Scala", category: "language", color: "#DC322F", icon: "scala" },
  { key: "r", label: "R", category: "language", color: "#276DC3", icon: "r" },
  { key: "shell", label: "Shell", category: "language", color: "#89E051", icon: "gnubash" },

  // ==========================================================================
  // FRONTEND
  // ==========================================================================
  { key: "react", label: "React", category: "frontend", color: "#61DAFB", icon: "react" },
  { key: "nextjs", label: "Next.js", category: "frontend", color: "#000000", icon: "nextdotjs" },
  { key: "vue", label: "Vue.js", category: "frontend", color: "#4FC08D", icon: "vuedotjs" },
  { key: "nuxt", label: "Nuxt", category: "frontend", color: "#00DC82", icon: "nuxtdotjs" },
  { key: "svelte", label: "Svelte", category: "frontend", color: "#FF3E00", icon: "svelte" },
  { key: "angular", label: "Angular", category: "frontend", color: "#DD0031", icon: "angular" },
  { key: "jquery", label: "jQuery", category: "frontend", color: "#0769AD", icon: "jquery" },
  { key: "html", label: "HTML", category: "frontend", color: "#E34F26", icon: "html5" },
  { key: "css", label: "CSS", category: "frontend", color: "#1572B6", icon: "css3" },
  { key: "sass", label: "Sass", category: "frontend", color: "#CC6699", icon: "sass" },
  { key: "tailwind", label: "Tailwind CSS", category: "frontend", color: "#06B6D4", icon: "tailwindcss" },
  { key: "bootstrap", label: "Bootstrap", category: "frontend", color: "#7952B3", icon: "bootstrap" },
  { key: "styled-components", label: "Styled Components", category: "frontend", color: "#DB7093", icon: "styledcomponents" },
  { key: "vite", label: "Vite", category: "frontend", color: "#646CFF", icon: "vite" },

  // ==========================================================================
  // MOBILE
  // ==========================================================================
  { key: "react-native", label: "React Native", category: "mobile", color: "#61DAFB", icon: "react" },
  { key: "flutter", label: "Flutter", category: "mobile", color: "#02569B", icon: "flutter" },
  { key: "android", label: "Android", category: "mobile", color: "#3DDC84", icon: "android" },
  { key: "ios", label: "iOS", category: "mobile", color: "#000000", icon: "ios" },
  { key: "swiftui", label: "SwiftUI", category: "mobile", color: "#FA7343", icon: "swift" },

  // ==========================================================================
  // BACKEND
  // ==========================================================================
  { key: "nodejs", label: "Node.js", category: "backend", color: "#339933", icon: "nodedotjs" },
  { key: "express", label: "Express", category: "backend", color: "#000000", icon: "express" },
  { key: "nest", label: "NestJS", category: "backend", color: "#E0234E", icon: "nestjs" },
  { key: "fastapi", label: "FastAPI", category: "backend", color: "#009688", icon: "fastapi" },
  { key: "django", label: "Django", category: "backend", color: "#092E20", icon: "django" },
  { key: "flask", label: "Flask", category: "backend", color: "#000000", icon: "flask" },
  { key: "spring", label: "Spring", category: "backend", color: "#6DB33F", icon: "spring" },
  { key: "spring-boot", label: "Spring Boot", category: "backend", color: "#6DB33F", icon: "springboot" },
  { key: "laravel", label: "Laravel", category: "backend", color: "#FF2D20", icon: "laravel" },
  { key: "ruby-on-rails", label: "Ruby on Rails", category: "backend", color: "#CC0000", icon: "rubyonrails" },
  { key: "aspnet", label: "ASP.NET", category: "backend", color: "#512BD4", icon: "dotnet" },
  { key: "grpc", label: "gRPC", category: "backend", color: "#244C5A", icon: "grpc" },

  // ==========================================================================
  // DATABASE
  // ==========================================================================
  { key: "mysql", label: "MySQL", category: "database", color: "#4479A1", icon: "mysql" },
  { key: "postgresql", label: "PostgreSQL", category: "database", color: "#336791", icon: "postgresql" },
  { key: "sqlite", label: "SQLite", category: "database", color: "#003B57", icon: "sqlite" },
  { key: "mariadb", label: "MariaDB", category: "database", color: "#C49A41", icon: "mariadb" },
  { key: "mongodb", label: "MongoDB", category: "database", color: "#47A248", icon: "mongodb" },
  { key: "redis", label: "Redis", category: "database", color: "#DC382D", icon: "redis" },
  { key: "elasticsearch", label: "Elasticsearch", category: "database", color: "#005571", icon: "elasticsearch" },
  { key: "dynamodb", label: "DynamoDB", category: "database", color: "#4053D6", icon: "amazondynamodb" },
  { key: "firebase-firestore", label: "Firebase Firestore", category: "database", color: "#FFCA28", icon: "firebase" },

  // ==========================================================================
  // INFRA / DEVOPS
  // ==========================================================================
  { key: "aws", label: "AWS", category: "infra", color: "#232F3E", icon: "amazonaws" },
  { key: "gcp", label: "Google Cloud", category: "infra", color: "#4285F4", icon: "googlecloud" },
  { key: "azure", label: "Azure", category: "infra", color: "#0078D4", icon: "microsoftazure" },
  { key: "docker", label: "Docker", category: "infra", color: "#2496ED", icon: "docker" },
  { key: "kubernetes", label: "Kubernetes", category: "infra", color: "#326CE5", icon: "kubernetes" },
  { key: "nginx", label: "Nginx", category: "infra", color: "#009639", icon: "nginx" },
  { key: "apache", label: "Apache", category: "infra", color: "#D22128", icon: "apache" },
  { key: "gitlab-ci", label: "GitLab CI", category: "infra", color: "#FC6D26", icon: "gitlab" },
  { key: "github-actions", label: "GitHub Actions", category: "infra", color: "#2088FF", icon: "githubactions" },
  { key: "jenkins", label: "Jenkins", category: "infra", color: "#D24939", icon: "jenkins" },
  { key: "vercel", label: "Vercel", category: "infra", color: "#000000", icon: "vercel" },
  { key: "netlify", label: "Netlify", category: "infra", color: "#00C7B7", icon: "netlify" },
  { key: "cloudflare", label: "Cloudflare", category: "infra", color: "#F38020", icon: "cloudflare" },

  // ==========================================================================
  // COLLABORATION
  // ==========================================================================
  { key: "git", label: "Git", category: "collaboration", color: "#F05032", icon: "git" },
  { key: "github", label: "GitHub", category: "collaboration", color: "#181717", icon: "github" },
  { key: "gitlab", label: "GitLab", category: "collaboration", color: "#FC6D26", icon: "gitlab" },
  { key: "bitbucket", label: "Bitbucket", category: "collaboration", color: "#0052CC", icon: "bitbucket" },
  { key: "jira", label: "Jira", category: "collaboration", color: "#0052CC", icon: "jira" },
  { key: "notion", label: "Notion", category: "collaboration", color: "#000000", icon: "notion" },
  { key: "slack", label: "Slack", category: "collaboration", color: "#4A154B", icon: "slack" },
  { key: "discord", label: "Discord", category: "collaboration", color: "#5865F2", icon: "discord" },

  // ==========================================================================
  // AI / ML
  // ==========================================================================
  { key: "pandas", label: "Pandas", category: "ai-ml", color: "#150458", icon: "pandas" },
  { key: "numpy", label: "NumPy", category: "ai-ml", color: "#013243", icon: "numpy" },
  { key: "scikit-learn", label: "Scikit-learn", category: "ai-ml", color: "#F7931E", icon: "scikitlearn" },
  { key: "tensorflow", label: "TensorFlow", category: "ai-ml", color: "#FF6F00", icon: "tensorflow" },
  { key: "pytorch", label: "PyTorch", category: "ai-ml", color: "#EE4C2C", icon: "pytorch" },
  { key: "opencv", label: "OpenCV", category: "ai-ml", color: "#5C3EE8", icon: "opencv" },
  { key: "yolov5", label: "YOLOv5", category: "ai-ml", color: "#00A8FF" },
  { key: "yolov8", label: "YOLOv8", category: "ai-ml", color: "#00A8FF" },
  { key: "huggingface", label: "Hugging Face", category: "ai-ml", color: "#FFD21E", icon: "huggingface" },
  { key: "transformers", label: "Transformers", category: "ai-ml", color: "#FFD21E" },

  // ==========================================================================
  // TESTING
  // ==========================================================================
  { key: "jest", label: "Jest", category: "testing", color: "#C21325", icon: "jest" },
  { key: "react-testing-library", label: "React Testing Library", category: "testing", color: "#E33332" },
  { key: "cypress", label: "Cypress", category: "testing", color: "#17202C", icon: "cypress" },
  { key: "playwright", label: "Playwright", category: "testing", color: "#2EAD33", icon: "playwright" },
  { key: "pytest", label: "pytest", category: "testing", color: "#0A9EDC", icon: "pytest" },
  { key: "junit", label: "JUnit", category: "testing", color: "#25A162", icon: "junit" },

  // ==========================================================================
  // TOOLING
  // ==========================================================================
  { key: "webpack", label: "Webpack", category: "tool", color: "#8DD6F9", icon: "webpack" },
  { key: "rollup", label: "Rollup", category: "tool", color: "#EC4A3F", icon: "rollupdotjs" },
  { key: "esbuild", label: "esbuild", category: "tool", color: "#FFCF00" },
  { key: "babel", label: "Babel", category: "tool", color: "#F9DC3E", icon: "babel" },
  { key: "eslint", label: "ESLint", category: "tool", color: "#4B32C3", icon: "eslint" },
  { key: "prettier", label: "Prettier", category: "tool", color: "#F7B93E", icon: "prettier" },
  { key: "npm", label: "npm", category: "tool", color: "#CB3837", icon: "npm" },
  { key: "yarn", label: "Yarn", category: "tool", color: "#2C8EBB", icon: "yarn" },
  { key: "pnpm", label: "pnpm", category: "tool", color: "#F69220", icon: "pnpm" },
];

/**
 * Fast lookup map: stack key → StackMeta
 * Use this for O(1) lookups when you have a key.
 */
export const STACK_META_MAP: ReadonlyMap<string, StackMeta> = new Map(
  STACK_META_LIST.map((meta) => [meta.key, meta])
);

/**
 * Grouped stacks by category: category → StackMeta[]
 * Use this to get all stacks in a specific category.
 */
export const STACKS_BY_CATEGORY: ReadonlyMap<StackCategory, StackMeta[]> = (() => {
  const map = new Map<StackCategory, StackMeta[]>();
  
  // Initialize all categories with empty arrays
  const categories: StackCategory[] = [
    "language",
    "frontend",
    "mobile",
    "backend",
    "database",
    "infra",
    "collaboration",
    "ai-ml",
    "testing",
    "tool",
  ];
  
  categories.forEach((cat) => {
    map.set(cat, []);
  });
  
  // Group stacks by category
  STACK_META_LIST.forEach((meta) => {
    const existing = map.get(meta.category) || [];
    existing.push(meta);
    map.set(meta.category, existing);
  });
  
  return map;
})();

/**
 * Get stack metadata by key.
 * 
 * @param key - Stack key (e.g., "react", "fastapi")
 * @returns StackMeta if found, undefined otherwise
 * 
 * @example
 * ```ts
 * const meta = getStackMeta("react");
 * // { key: "react", label: "React", category: "frontend", color: "#61DAFB" }
 * ```
 */
export function getStackMeta(key: string): StackMeta | undefined {
  return STACK_META_MAP.get(key);
}

/**
 * Get all stacks in a specific category.
 * 
 * @param category - Stack category
 * @returns Array of StackMeta for the given category
 * 
 * @example
 * ```ts
 * const frontendStacks = getStacksByCategory("frontend");
 * // Returns all frontend stack metadata
 * ```
 */
export function getStacksByCategory(category: StackCategory): StackMeta[] {
  return STACKS_BY_CATEGORY.get(category) || [];
}

/**
 * Get all available stack keys.
 * 
 * @returns Array of all stack keys
 */
export function getAllStackKeys(): string[] {
  return STACK_META_LIST.map((meta) => meta.key);
}

/**
 * Get all available categories.
 * 
 * @returns Array of all stack categories
 */
export function getAllCategories(): StackCategory[] {
  return Array.from(STACKS_BY_CATEGORY.keys());
}

/**
 * Check if a stack key exists.
 * 
 * @param key - Stack key to check
 * @returns true if the key exists, false otherwise
 */
export function hasStackKey(key: string): boolean {
  return STACK_META_MAP.has(key);
}

