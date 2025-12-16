import React, { useState, useEffect } from 'react';
import { Button } from '../../../shared/components/Button';
import styles from './MarkdownBadgeSection.module.css';

interface MarkdownBadgeSectionProps {
  githubLogin: string;
  cardId: number;
}

export const MarkdownBadgeSection: React.FC<MarkdownBadgeSectionProps> = ({
  githubLogin,
  cardId,
}) => {
  const [readmeTemplate, setReadmeTemplate] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [readmeCopied, setReadmeCopied] = useState(false);
  const [linkCopied, setLinkCopied] = useState(false);
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const FRONTEND_BASE_URL = import.meta.env.VITE_FRONTEND_BASE_URL || 'http://3.37.130.140';
  const publicCardUrl = `${FRONTEND_BASE_URL}/dashboard/${githubLogin}/cards/${cardId}`;

  useEffect(() => {
    loadReadmeTemplate();
  }, [githubLogin, cardId]);

  const loadReadmeTemplate = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/profiles/public/${githubLogin}/cards/${cardId}/readme`
      );
      if (response.ok) {
        const text = await response.text();
        setReadmeTemplate(text.trim());
      }
    } catch (error) {
      console.error('README 템플릿 로드 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = async (text: string): Promise<boolean> => {
    // 최신 브라우저 API 시도
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch (error) {
        console.warn('Clipboard API 실패, fallback 사용:', error);
      }
    }

    // Fallback: 텍스트 영역 생성하여 복사
    try {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      textArea.style.top = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      
      const successful = document.execCommand('copy');
      document.body.removeChild(textArea);
      
      if (successful) {
        return true;
      } else {
        throw new Error('execCommand 실패');
      }
    } catch (error) {
      console.error('복사 실패:', error);
      return false;
    }
  };

  const handleCopyReadmeTemplate = async () => {
    const success = await copyToClipboard(readmeTemplate);
    if (success) {
      setReadmeCopied(true);
      setTimeout(() => setReadmeCopied(false), 2000);
    } else {
      alert('README 템플릿 복사에 실패했습니다. 아래 코드를 수동으로 선택하여 복사해주세요.');
    }
  };

  const handleCopyLink = async () => {
    const success = await copyToClipboard(publicCardUrl);
    if (success) {
      setLinkCopied(true);
      setTimeout(() => setLinkCopied(false), 2000);
    } else {
      alert('링크 복사에 실패했습니다. 아래 링크를 수동으로 선택하여 복사해주세요.');
    }
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>로딩 중...</div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>📋 GitHub README에 추가하기</h3>
      <p className={styles.description}>
        아래 코드를 복사하여 GitHub README.md 파일에 붙여넣으세요.
      </p>

      {/* README 템플릿 섹션 */}
      <div className={styles.codeSection}>
        <div className={styles.codeHeader}>
          <span className={styles.codeLabel}>📝 README 템플릿:</span>
          <Button
            onClick={handleCopyReadmeTemplate}
            variant={readmeCopied ? 'primary' : 'secondary'}
            className={styles.copyButton}
          >
            {readmeCopied ? '✓ README 템플릿 복사됨!' : '📋 README 템플릿 복사'}
          </Button>
        </div>
        <div className={styles.codeBlock}>
          <code className={styles.code}>{readmeTemplate || '로딩 중...'}</code>
        </div>
        <p className={styles.infoText}>
          💡 <strong>README 템플릿</strong>은 GitHub README에서 안정적으로 렌더링되도록 설계되었습니다.
          SVG 배너, shields.io 배지, github-readme-stats를 사용합니다.
        </p>
      </div>

      <div className={styles.linkSection}>
        <div className={styles.linkHeader}>
          <span className={styles.linkLabel}>🔗 공개 프로필 카드 링크:</span>
          <div className={styles.linkActions}>
            <Button
              onClick={handleCopyLink}
              variant={linkCopied ? 'primary' : 'secondary'}
              className={styles.copyLinkButton}
            >
              {linkCopied ? '✓ 링크 복사됨!' : '📋 링크 복사'}
            </Button>
            <a
              href={publicCardUrl}
              target="_blank"
              rel="noopener noreferrer"
              className={styles.viewLink}
            >
              <Button variant="secondary" className={styles.viewButton}>
                👁️ 새 창에서 보기
              </Button>
            </a>
          </div>
        </div>
        <div className={styles.linkBlock}>
          <code className={styles.linkCode}>{publicCardUrl}</code>
        </div>
      </div>

      <div className={styles.infoBox}>
        <strong>💡 사용 방법:</strong>
        <ol className={styles.instructions}>
          <li><strong>README 템플릿:</strong> 위의 "README 템플릿" 코드를 복사하여 README.md에 붙여넣으세요. GitHub에서 안정적으로 렌더링됩니다.</li>
        </ol>
      </div>
    </div>
  );
};
