import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

interface AuthModalProps {
  apiUrl?: string;
}

interface User {
  id: string;
  email: string;
  name: string;
  experience_level: string;
}

export default function AuthModal({ apiUrl = 'http://localhost:8000' }: AuthModalProps): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);

  // Form state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('beginner');
  const [programmingLanguages, setProgrammingLanguages] = useState<string[]>([]);
  const [roboticsExperience, setRoboticsExperience] = useState(false);
  const [learningGoals, setLearningGoals] = useState('');

  // Check for existing session on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const savedUser = localStorage.getItem('user');
    if (token && savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const endpoint = isLogin ? '/api/auth/login' : '/api/auth/signup';
      const body = isLogin
        ? { email, password }
        : {
          email,
          password,
          name,
          experience_level: experienceLevel,
          programming_languages: programmingLanguages,
          robotics_experience: roboticsExperience,
          learning_goals: learningGoals.split(',').map(g => g.trim()).filter(Boolean)
        };

      const response = await fetch(`${apiUrl}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      // Store tokens and user data
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      localStorage.setItem('userLevel', data.user.experience_level);

      setUser(data.user);
      setIsOpen(false);

      // Reset form
      setEmail('');
      setPassword('');
      setName('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  const toggleLanguage = (lang: string) => {
    setProgrammingLanguages(prev =>
      prev.includes(lang) ? prev.filter(l => l !== lang) : [...prev, lang]
    );
  };

  if (user) {
    return (
      <div className={styles.userInfo}>
        <span className={styles.userName}>👤 {user.name}</span>
        <span className={styles.userLevel}>{user.experience_level}</span>
        <button onClick={handleLogout} className={styles.logoutBtn}>Logout</button>
      </div>
    );
  }

  return (
    <>
      <button onClick={() => setIsOpen(true)} className={styles.authButton}>
        🔐 Login / Sign Up
      </button>

      {isOpen && (
        <div className={styles.overlay} onClick={() => setIsOpen(false)}>
          <div className={styles.modal} onClick={e => e.stopPropagation()}>
            <button className={styles.closeBtn} onClick={() => setIsOpen(false)}>×</button>

            <h2 className={styles.title}>{isLogin ? 'Welcome Back!' : 'Create Account'}</h2>

            {error && <div className={styles.error}>{error}</div>}

            <form onSubmit={handleSubmit} className={styles.form}>
              {!isLogin && (
                <input
                  type="text"
                  placeholder="Your Name"
                  value={name}
                  onChange={e => setName(e.target.value)}
                  required
                  className={styles.input}
                />
              )}

              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                className={styles.input}
              />

              <input
                type="password"
                placeholder="Password (min 8 characters)"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
                minLength={8}
                className={styles.input}
              />

              {!isLogin && (
                <>
                  <div className={styles.fieldGroup}>
                    <label className={styles.label}>Experience Level</label>
                    <div className={styles.levelButtons}>
                      {['beginner', 'intermediate', 'advanced'].map(level => (
                        <button
                          key={level}
                          type="button"
                          className={`${styles.levelBtn} ${experienceLevel === level ? styles.active : ''}`}
                          onClick={() => setExperienceLevel(level)}
                        >
                          {level === 'beginner' ? '🌱' : level === 'intermediate' ? '🌿' : '🌳'} {level}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className={styles.fieldGroup}>
                    <label className={styles.label}>Programming Languages</label>
                    <div className={styles.langButtons}>
                      {['Python', 'C++', 'JavaScript', 'Rust', 'Other'].map(lang => (
                        <button
                          key={lang}
                          type="button"
                          className={`${styles.langBtn} ${programmingLanguages.includes(lang) ? styles.active : ''}`}
                          onClick={() => toggleLanguage(lang)}
                        >
                          {lang}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className={styles.fieldGroup}>
                    <label className={styles.checkboxLabel}>
                      <input
                        type="checkbox"
                        checked={roboticsExperience}
                        onChange={e => setRoboticsExperience(e.target.checked)}
                      />
                      I have prior robotics experience
                    </label>
                  </div>

                  <input
                    type="text"
                    placeholder="Learning goals (comma separated)"
                    value={learningGoals}
                    onChange={e => setLearningGoals(e.target.value)}
                    className={styles.input}
                  />
                </>
              )}

              <button type="submit" className={styles.submitBtn} disabled={isLoading}>
                {isLoading ? '⏳ Please wait...' : (isLogin ? 'Login' : 'Create Account')}
              </button>
            </form>

            <p className={styles.switchText}>
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button
                type="button"
                className={styles.switchBtn}
                onClick={() => { setIsLogin(!isLogin); setError(null); }}
              >
                {isLogin ? 'Sign Up' : 'Login'}
              </button>
            </p>
          </div>
        </div>
      )}
    </>
  );
}

