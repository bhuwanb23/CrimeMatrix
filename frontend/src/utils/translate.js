// Simple translation utility for CrimeMatrix UI
// Languages: en (English), ta (Tamil), kn (Kannada), te (Telugu), hi (Hindi)

const translations = {
    en: {
      accept: "Accept",
      dismiss: "Dismiss",
      view: "View",
      alert: "Alert",
      priority: "Priority",
      status: "Status",
      alerts: "alerts",
      alert_feed: "Alert Feed"
    },
    ta: {
      accept: "ஒப்புக்கொள்",
      dismiss: "நிராகரி",
      view: "பார்",
      alert: "எச்சரிக்கை",
      priority: "முன்னுரிமை",
      status: "நிலை",
      alerts: "அவசரங்கள்",
      alert_feed: "அவசரப் புலம்"
    },
    kn: {
      accept: "ಸ್ವೀಕರಿಸಿ",
      dismiss: "ಮುಂದುವರಿಕೆ",
      view: "ವೀಕ್ಷಿಸು",
      alert: "ಎಚ್ಚರಿಕೆ",
      priority: "ಪ್ರಾಮುಖ್ಯತೆಯ",
      status: "ಸ್ಥಿತಿ",
      alerts: "ಎಚ್ಚರಿಕೆಗಳು",
      alert_feed: "ಎಚ್ಚರಿಕಾ ಫೀಡ್"
    },
    te: {
      accept: "అంగీకరించండి",
      dismiss: "నిరాకరించండి",
      view: "వీక్షించండి",
      alert: "అలర్ట్",
      priority: "ప్రాధాన్యత",
      status: "స్థితి",
      alerts: "అలర్ట్స్",
      alert_feed: "అలర్ట్ ఫీడ్"
    },
    hi: {
      accept: "स्वीकार करें",
      dismiss: "अस्वीकार",
      view: "देखें",
      alert: "अलर्ट",
      priority: "प्राथमिकता",
      status: "स्थिति",
      alerts: "अलर्ट्स",
      alert_feed: "अलर्ट फ़ीड"
    },
};

/**
 * Translate a key based on the provided language code.
 * @param {string} key - The translation key.
 * @param {string} [lang='en'] - Language code (en, ta, kn, te, hi).
 * @returns {string} Translated string or the key if missing.
 */
export function t(key, lang = "en") {
  const langDict = translations[lang] || translations.en;
  return langDict[key] || key;
}

// Export list of supported languages for UI selectors
export const supportedLanguages = ["en", "ta", "kn", "te", "hi"];
