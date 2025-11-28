import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget';

// API URL - can be configured via docusaurus.config.ts customFields
const API_URL = 'http://localhost:8000';

// Default implementation, that you can customize
export default function Root({children}: {children: React.ReactNode}): JSX.Element {
  return (
    <>
      {children}
      <ChatWidget apiUrl={API_URL} />
    </>
  );
}

