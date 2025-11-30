import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatWidgetProps {
  apiUrl?: string;
}

export default function ChatWidget({ apiUrl = 'http://localhost:8000' }: ChatWidgetProps): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Speech Recognition Setup
  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Initialize Speech Synthesis
      synthRef.current = window.speechSynthesis;

      // Initialize Speech Recognition
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = false;
        recognitionRef.current.interimResults = false;
        recognitionRef.current.lang = 'en-US';

        recognitionRef.current.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setInput(transcript);
          setIsListening(false);
          // Auto-send after voice input
          setTimeout(() => sendMessage(transcript), 500);
        };

        recognitionRef.current.onerror = (event: any) => {
          console.error('Speech recognition error', event.error);
          setIsListening(false);
        };

        recognitionRef.current.onend = () => {
          setIsListening(false);
        };
      }
    }
  }, []);

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      recognitionRef.current?.start();
      setIsListening(true);
    }
  };

  const speakText = (text: string) => {
    if (synthRef.current) {
      if (isSpeaking) {
        synthRef.current.cancel();
        setIsSpeaking(false);
        return;
      }
      
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.onend = () => setIsSpeaking(false);
      setIsSpeaking(true);
      synthRef.current.speak(utterance);
    }
  };

  // Listen for text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim().length > 0) {
        setSelectedText(selection.toString().trim());
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (question: string) => {
    if (!question.trim()) return;

    const userMessage: Message = { role: 'user', content: question };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Get user background for personalization
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      const userLevel = localStorage.getItem('userLevel') || 'intermediate';

      const response = await fetch(`${apiUrl}/api/chat/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question,
          selected_text: selectedText || null,
          chapter_context: document.title,
          user_level: userLevel,
          programming_languages: user.programming_languages || [],
          robotics_experience: user.robotics_experience || false,
          learning_goals: user.learning_goals || []
        })
      });

      const data = await response.json();
      const assistantMessage: Message = { role: 'assistant', content: data.answer };
      setMessages(prev => [...prev, assistantMessage]);
      
      // Auto-speak the answer if it was a voice query (optional, but cool)
      // speakText(data.answer); 
    } catch (error: any) {
      let errorText = 'Sorry, I encountered an error. Please try again.';

      // Check for rate limit error
      if (error?.message?.includes('429') || error?.message?.includes('rate')) {
        errorText = '⏳ OpenAI rate limit reached. Please wait 1-2 minutes and try again. (Free tier limitation)';
      }

      const errorMessage: Message = {
        role: 'assistant',
        content: errorText
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setSelectedText('');
    }
  };

  const askAboutSelection = () => {
    if (selectedText) {
      sendMessage(`Explain this: "${selectedText}"`);
    }
  };

  return (
    <>
      {/* Floating Ask AI Button (shows when text is selected) */}
      {selectedText && !isOpen && (
        <button className={styles.askButton} onClick={askAboutSelection}>
          🤖 Ask AI about selection
        </button>
      )}

      {/* Chat Toggle Button */}
      <button className={styles.toggleButton} onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.header}>
            <span>🤖 AI Assistant</span>
            <span className={styles.hint}>Select text to ask about it!</span>
          </div>

          <div className={styles.messages}>
            {messages.length === 0 && (
              <div className={styles.welcome}>
                <p>👋 Hi! I'm your AI learning assistant.</p>
                <p>Ask me anything about Physical AI, ROS 2, Gazebo, or VLA models!</p>
                <p><strong>Tip:</strong> Select any text on the page and click "Ask AI".</p>
              </div>
            )}
            {messages.map((msg, idx) => (
              <div key={idx} className={`${styles.message} ${styles[msg.role]}`}>
                {msg.content}
                {msg.role === 'assistant' && (
                  <button 
                    className={styles.speakButton} 
                    onClick={() => speakText(msg.content)}
                    title="Read aloud"
                  >
                    {isSpeaking && messages[messages.length-1] === msg ? '🔇' : '🔊'}
                  </button>
                )}
              </div>
            ))}
            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <span className={styles.typing}>Thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.inputArea}>
            <button 
              className={`${styles.micButton} ${isListening ? styles.listening : ''}`}
              onClick={toggleListening}
              title="Speak your question"
            >
              {isListening ? '🛑' : '🎤'}
            </button>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage(input)}
              placeholder={isListening ? "Listening..." : "Ask a question..."}
              disabled={isLoading}
            />
            <button onClick={() => sendMessage(input)} disabled={isLoading || !input.trim()}>
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
}

