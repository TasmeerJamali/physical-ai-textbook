import React, { useState } from 'react';
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

  const getPageContent = (): string => {
    const article = document.querySelector('article');
    return article?.innerHTML || '';
  };

  const handlePersonalize = async () => {
    setIsPersonalizing(true);
    try {
      const content = getPageContent();
      const response = await fetch(`${apiUrl}/api/personalize/adapt`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content,
          chapter_id: chapterId,
          user_level: localStorage.getItem('userLevel') || 'intermediate',
          user_background: JSON.parse(localStorage.getItem('userBackground') || '{}')
        })
      });
      const data = await response.json();
      setPersonalizedContent(data.personalized_content);
      
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
    if (showUrdu && translatedContent) {
      // Toggle back to English
      const article = document.querySelector('article');
      if (article && personalizedContent) {
        article.innerHTML = personalizedContent;
      } else {
        window.location.reload();
      }
      setShowUrdu(false);
      return;
    }

    setIsTranslating(true);
    try {
      const content = getPageContent();
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
      <button 
        className={styles.button}
        onClick={handlePersonalize}
        disabled={isPersonalizing}
        title="Personalize content based on your experience level"
      >
        {isPersonalizing ? '⏳' : '✨'} Personalize
      </button>
      
      <button 
        className={`${styles.button} ${showUrdu ? styles.active : ''}`}
        onClick={handleTranslate}
        disabled={isTranslating}
        title="Translate to Urdu"
      >
        {isTranslating ? '⏳' : '🌐'} {showUrdu ? 'English' : 'اردو'}
      </button>
    </div>
  );
}

