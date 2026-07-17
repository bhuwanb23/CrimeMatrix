import React, { createContext, useState, useContext } from 'react';

// LanguageContext provides current UI language and a setter
export const LanguageContext = createContext({
  lang: 'en',
  setLang: () => {},
});

export const LanguageProvider = ({ children }) => {
  const [lang, setLang] = useState('en');
  return (
    <LanguageContext.Provider value={{ lang, setLang }}>
      {children}
    </LanguageContext.Provider>
  );
};

// Helper hook for consuming the context
export const useLanguage = () => useContext(LanguageContext);
