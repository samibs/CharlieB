import React from 'react';
import ChatWidget from './ChatWidget';

const App = () => {
  return (
    <div className="font-sans min-h-screen">
      <h1 className="text-center text-3xl font-bold mt-8">Welcome to CharlieB</h1>
      <ChatWidget />
    </div>
  );
};

export default App;