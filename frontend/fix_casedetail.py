import codecs

content = """import { useLanguage } from '../context/LanguageContext'
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getCaseById } from './search/caseData'
import {
  ArrowLeft, Clock, User, FileText, Shield, AlertTriangle,
  Camera, Bot, MapPin, Calendar, Hash,
} from 'lucide-react'
import SimilarCasesPanel from './similar/SimilarCasesPanel'
import FIRSuggestionsPanel from './case-detail/FIRSuggestionsPanel'
import BookmarkButton from './bookmarks/BookmarkButton'

const timelineIcons = {
  filing: FileText,
  investigation: Shield,
  evidence: Camera,
  suspect: AlertTriangle,
}

export default function CaseDetailPage() {
  const { t } = useLanguage()
  const { id } = useParams()
  const navigate = useNavigate()
  const caseData = getCaseById(id, t)

  if (!caseData) {
    return (
      <div className="case-detail-empty">
        <h2>{t('Case not found')}</h2>
        <p>No case found with ID: {id}</p>
        <button className="case-back-btn" onClick={() => navigate('/cases')}>
          <ArrowLeft size={16} /> {t('Back to Search')}
        </button>
      </div>
    )
  }

  return (
    <div className="case-detail">
      {/* Header */}
      <div className="case-header">
        <button className="case-back-btn" onClick={() => navigate('/cases')}>
          <ArrowLeft size={16} /> {t('Back to Search')}
        </button>
"""

with codecs.open(r'e:\CrimeMatrix\frontend\src\components\CaseDetailPage.jsx', 'r', 'utf-8') as f:
    text = f.read()

idx_header = text.find('<div className="case-header-info">')

new_text = content + text[idx_header:]

with codecs.open(r'e:\CrimeMatrix\frontend\src\components\CaseDetailPage.jsx', 'w', 'utf-8') as f:
    f.write(new_text)

print('Fixed CaseDetailPage.jsx')
