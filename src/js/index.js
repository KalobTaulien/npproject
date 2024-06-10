import React from 'react';
import App from './app/App';
import { createRoot } from 'react-dom/client';

// Look for #app in the DOM. If it exists, render the App component.
const container = document.getElementById('app') || false;
if(container) {
  const root = createRoot(container);
  root.render(<App />);
}
