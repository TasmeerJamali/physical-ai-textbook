import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

interface ContentActionsProps {
  chapterId: string;
  apiUrl?: string;
}

export default function ContentActions({
  chapterId,
  apiUrl = 'http://localhost:8000'
}: ContentActionsProps): JSX.Element {
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [showUrdu, setShowUrdu] = useState(false);
  const [personalizedContent, setPersonalizedContent] = useState<string | null>(null);
  const [translatedContent, setTranslatedContent] = useState<string | null>(null);
  const [originalContent, setOriginalContent] = useState<string | null>(null);
  const [userLevel, setUserLevel] = useState<string>('intermediate');
  const [isPersonalized, setIsPersonalized] = useState(false);

  // Load user level from localStorage on mount
  useEffect(() => {
    const savedLevel = localStorage.getItem('userLevel');
    if (savedLevel) {
      setUserLevel(savedLevel);
    }
  }, []);

  // Save user level to localStorage when changed
  const handleLevelChange = (level: string) => {
    setUserLevel(level);
    localStorage.setItem('userLevel', level);
  };

  const getPageContent = (): string => {
    const article = document.querySelector('article');
    return article?.innerHTML || '';
  };

  const handlePersonalize = async () => {
    // If already personalized, restore original
    if (isPersonalized) {
      const article = document.querySelector('article');
      if (article && originalContent) {
        article.innerHTML = originalContent;
      }
      setIsPersonalized(false);
      setPersonalizedContent(null);
      return;
    }

    setIsPersonalizing(true);
    try {
      const content = getPageContent();
      if (!originalContent) {
        setOriginalContent(content);
      }
      const response = await fetch(`${apiUrl}/api/personalize/adapt`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content,
          chapter_id: chapterId,
          user_level: userLevel,
          user_background: JSON.parse(localStorage.getItem('userBackground') || '{}')
        })
      });
      const data = await response.json();
      setPersonalizedContent(data.personalized_content);
      setIsPersonalized(true);

      // Update the page content
      const article = document.querySelector('article');
      if (article) {
        article.innerHTML = data.personalized_content;
      }
    } catch (error) {
      console.error('Personalization failed:', error);
    } finally {
      setIsPersonalizing(false);
    }
  };

  const handleTranslate = async () => {
    if (showUrdu) {
      // Toggle back to English
      const article = document.querySelector('article');
      if (article) {
        if (personalizedContent) {
          article.innerHTML = personalizedContent;
        } else if (originalContent) {
          article.innerHTML = originalContent;
        } else {
          window.location.reload();
        }
        article.dir = 'ltr'; // Back to left-to-right for English
      }
      setShowUrdu(false);
      return;
    }

    setIsTranslating(true);
    try {
      const content = getPageContent();
      if (!originalContent) {
        setOriginalContent(content);
      }
      const response = await fetch(`${apiUrl}/api/personalize/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content,
          target_language: 'ur',
          preserve_code: true
        })
      });
      const data = await response.json();
      setTranslatedContent(data.translated_content);

      // Update the page content
      const article = document.querySelector('article');
      if (article) {
        article.innerHTML = data.translated_content;
        article.dir = 'rtl'; // Right-to-left for Urdu
      }
      setShowUrdu(true);
    } catch (error) {
      console.error('Translation failed:', error);
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <div className={styles.container}>
      {/* Loading message */}
      {(isPersonalizing || isTranslating) && (
        <div className={styles.loadingMessage}>
          ⏳ {isPersonalizing ? 'Personalizing' : 'Translating'}... This may take 20-30 seconds
        </div>
      )}

      {/* Level selector for personalization */}
      <div className={styles.levelSelector}>
        <span className={styles.levelLabel}>Your Level:</span>
        <div className={styles.levelButtons}>
          {['beginner', 'intermediate', 'advanced'].map((level) => (
            <button
              key={level}
              className={`${styles.levelButton} ${userLevel === level ? styles.levelButtonActive : ''}`}
              onClick={() => handleLevelChange(level)}
              disabled={isPersonalizing || isTranslating}
            >
              {level === 'beginner' ? '🌱' : level === 'intermediate' ? '🌿' : '🌳'} {level.charAt(0).toUpperCase() + level.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.buttonGroup}>
        <button
          className={`${styles.button} ${isPersonalized ? styles.activePersonalized : ''}`}
          onClick={handlePersonalize}
          disabled={isPersonalizing || isTranslating}
          title={isPersonalized ? "Restore original content" : "Personalize content based on your experience level"}
        >
          {isPersonalizing ? '⏳' : isPersonalized ? '🔙' : '✨'} {isPersonalized ? 'Back to Original' : 'Personalize'}
        </button>

        <button
          className={`${styles.button} ${showUrdu ? styles.activeUrdu : ''}`}
          onClick={handleTranslate}
          disabled={isTranslating || isPersonalizing}
          title={showUrdu ? "Switch back to English" : "Translate to Urdu"}
        >
          {isTranslating ? '⏳' : showUrdu ? '🔙' : '🌐'} {showUrdu ? 'Back to English' : 'اردو'}
        </button>
      </div>
    </div>
  );
}

