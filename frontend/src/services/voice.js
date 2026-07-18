const LANGUAGES = {
  en: { name: 'English', sttCode: 'en-US', ttsVoice: 'Google UK English Female' },
  kn: { name: 'Kannada', sttCode: 'kn-IN', ttsVoice: null },
  hi: { name: 'Hindi', sttCode: 'hi-IN', ttsVoice: null },
}

let recognition = null
let synthesis = window.speechSynthesis || null

export function isSTTSupported() {
  return 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window
}

export function isTTSSupported() {
  return 'speechSynthesis' in window
}

export function startListening(language = 'en', onResult, onEnd, onError) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!SpeechRecognition) {
    onError?.('Speech recognition not supported in this browser')
    return null
  }

  recognition = new SpeechRecognition()
  recognition.continuous = false
  recognition.interimResults = true
  recognition.lang = LANGUAGES[language]?.sttCode || 'en-US'
  recognition.maxAlternatives = 1

  recognition.onresult = (event) => {
    const result = event.results[event.results.length - 1]
    const transcript = result[0].transcript
    const isFinal = result.isFinal
    onResult?.(transcript, isFinal)
  }

  recognition.onend = () => {
    onEnd?.()
  }

  recognition.onerror = (event) => {
    onError?.(event.error)
  }

  recognition.start()
  return recognition
}

export function stopListening() {
  if (recognition) {
    recognition.stop()
    recognition = null
  }
}

export function speak(text, language = 'en', onEnd) {
  if (!synthesis) {
    onEnd?.()
    return
  }

  synthesis.cancel()

  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = LANGUAGES[language]?.sttCode || 'en-US'
  utterance.rate = 1.0
  utterance.pitch = 1.0

  const voices = synthesis.getVoices()
  const langVoice = voices.find(v => v.lang.startsWith(utterance.lang.split('-')[0]))
  if (langVoice) {
    utterance.voice = langVoice
  }

  utterance.onend = () => {
    onEnd?.()
  }

  utterance.onerror = () => {
    onEnd?.()
  }

  synthesis.speak(utterance)
}

export function stopSpeaking() {
  if (synthesis) {
    synthesis.cancel()
  }
}

export function getVoices() {
  if (!synthesis) return []
  return synthesis.getVoices()
}

export { LANGUAGES }
