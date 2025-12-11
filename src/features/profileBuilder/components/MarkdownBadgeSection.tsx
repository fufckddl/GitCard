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
  const [markdownBadge, setMarkdownBadge] = useState<string>('');
  const [htmlCode, setHtmlCode] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [htmlCopied, setHtmlCopied] = useState(false);
  const [linkCopied, setLinkCopied] = useState(false);
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const FRONTEND_BASE_URL = import.meta.env.VITE_FRONTEND_BASE_URL || 'http://3.37.130.140';
  const publicCardUrl = `${FRONTEND_BASE_URL}/dashboard/${githubLogin}/cards/${cardId}`;

  useEffect(() => {
    loadMarkdownBadge();
    loadHtml();
  }, [githubLogin, cardId]);

  const loadMarkdownBadge = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/profiles/public/${githubLogin}/cards/${cardId}/markdown/badge`
      );
      if (response.ok) {
        const text = await response.text();
        setMarkdownBadge(text.trim());
      }
    } catch (error) {
      console.error('마크다운 배지 로드 실패:', error);
    }
  };

  const loadHtml = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/profiles/public/${githubLogin}/cards/${cardId}/html`
      );
      if (response.ok) {
        const text = await response.text();
        setHtmlCode(text.trim());
      }
    } catch (error) {
      console.error('HTML 로드 실패:', error);
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

  const handleCopy = async () => {
    const success = await copyToClipboard(markdownBadge);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } else {
      // 수동 복사를 위한 텍스트 선택
      alert('자동 복사에 실패했습니다. 아래 코드를 수동으로 선택하여 복사해주세요.');
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

  const handleCopyHtml = async () => {
    const success = await copyToClipboard(htmlCode);
    if (success) {
      setHtmlCopied(true);
      setTimeout(() => setHtmlCopied(false), 2000);
    } else {
      alert('HTML 복사에 실패했습니다. 아래 HTML 코드를 수동으로 선택하여 복사해주세요.');
    }
  };

  const handleDownloadImage = async () => {
    try {
      const imageUrl = `${API_BASE_URL}/profiles/public/${githubLogin}/cards/${cardId}/image`;
      const response = await fetch(imageUrl);
      
      if (!response.ok) {
        throw new Error('이미지 다운로드 실패');
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `gitcard-${githubLogin}-${cardId}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('이미지 다운로드 실패:', error);
      alert('이미지 다운로드에 실패했습니다. Playwright가 서버에 설치되어 있는지 확인해주세요.');
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
        아래 마크다운 코드를 복사하여 GitHub README.md 파일에 붙여넣으세요.
      </p>
      
      <div className={styles.badgePreview}>
        <div className={styles.badgeHeader}>
          <div className={styles.badgeLabel}>미리보기:</div>
          <div className={styles.badgeActions}>
            <Button
              onClick={handleCopy}
              variant={copied ? 'primary' : 'secondary'}
              className={styles.previewButton}
            >
              {copied ? '✓ 마크다운 복사됨!' : '📋 마크다운 복사'}
            </Button>
            <Button
              onClick={handleDownloadImage}
              variant="secondary"
              className={styles.previewButton}
            >
              🖼️ 이미지 다운로드
            </Button>
          </div>
        </div>
        <div className={styles.badgeContent}>
          {markdownBadge ? (
            <a
              href={`${import.meta.env.VITE_FRONTEND_BASE_URL || 'http://3.37.130.140'}/dashboard/${githubLogin}/cards/${cardId}`}
              target="_blank"
              rel="noopener noreferrer"
              className={styles.badgeLink}
            >
              <img
                src={`${import.meta.env.VITE_FRONTEND_BASE_URL || 'http://3.37.130.140'}/dashboard/${githubLogin}/cards/${cardId}`}
                alt="GitCard"
                className={styles.badgeImage}
              />
            </a>
          ) : (
            <span className={styles.badgePlaceholder}>배지 미리보기</span>
          )}
        </div>
      </div>

      <div className={styles.codeSection}>
        <div className={styles.codeHeader}>
          <span className={styles.codeLabel}>마크다운 코드:</span>
          <Button
            onClick={handleCopy}
            variant={copied ? 'primary' : 'secondary'}
            className={styles.copyButton}
          >
            {copied ? '✓ 복사됨!' : '📋 복사'}
          </Button>
        </div>
        <div className={styles.codeBlock}>
          <code className={styles.code}>{markdownBadge || '로딩 중...'}</code>
        </div>
      </div>

      <div className={styles.codeSection}>
        <div className={styles.codeHeader}>
          <span className={styles.codeLabel}>HTML 코드 (독립 실행 가능):</span>
          <Button
            onClick={handleCopyHtml}
            variant={htmlCopied ? 'primary' : 'secondary'}
            className={styles.copyButton}
          >
            {htmlCopied ? '✓ HTML 복사됨!' : '📋 HTML 복사'}
          </Button>
        </div>
        <div className={styles.codeBlock}>
          <code className={styles.code}>{htmlCode || '로딩 중...'}</code>
        </div>
        <p className={styles.htmlNote}>
          💡 이 HTML 코드는 GitHub README.md에 직접 삽입하여 사용할 수 있습니다. 인라인 스타일로 작성되어 외부 의존성 없이 작동합니다.
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
          <li>위의 "복사" 버튼을 클릭하여 마크다운 코드를 복사합니다.</li>
          <li>GitHub 저장소의 README.md 파일을 엽니다.</li>
          <li>원하는 위치에 복사한 코드를 붙여넣습니다.</li>
          <li>변경사항을 커밋하고 푸시하면 README에 프로필 카드가 표시됩니다.</li>
        </ol>
      </div>
    </div>
  );
};
