import { useLanguage } from '../../context/LanguageContext'
import { MapPin, Phone, User, Hash } from 'lucide-react'

export default function ProfileTab({ suspect }) {
  const { t } = useLanguage()
  return (
    <div className="profile-tab">
      <div className="profile-grid">
        <div className="profile-section">
          <h4 className="profile-section-title">{t('Personal Information')}</h4>
          <div className="profile-info-list">
            <div className="profile-info-row">
              <User size={14} />
              <span className="profile-info-label">{t('Full Name')}</span>
              <span className="profile-info-value">{suspect.name}</span>
            </div>
            <div className="profile-info-row">
              <Hash size={14} />
              <span className="profile-info-label">{t('Age')}</span>
              <span className="profile-info-value">{suspect.age} years</span>
            </div>
            <div className="profile-info-row">
              <MapPin size={14} />
              <span className="profile-info-label">{t('District')}</span>
              <span className="profile-info-value">{suspect.district}</span>
            </div>
            <div className="profile-info-row">
              <Phone size={14} />
              <span className="profile-info-label">{t('Phone')}</span>
              <span className="profile-info-value">{suspect.phone}</span>
            </div>
          </div>
        </div>

        <div className="profile-section">
          <h4 className="profile-section-title">{t('Known Aliases')}</h4>
          <div className="profile-tags">
            {suspect.aliases.map((alias, i) => (
              <span key={i} className="profile-tag">{alias}</span>
            ))}
          </div>
        </div>

        <div className="profile-section">
          <h4 className="profile-section-title">{t('Address')}</h4>
          <p className="profile-address">{suspect.address}</p>
        </div>

        <div className="profile-section full-width">
          <h4 className="profile-section-title">{t('Physical Description')}</h4>
          <p className="profile-description">{suspect.physicalDescription}</p>
        </div>

        <div className="profile-section full-width">
          <h4 className="profile-section-title">{t('Criminal Summary')}</h4>
          <p className="profile-description">{suspect.description}</p>
        </div>
      </div>
    </div>
  )
}
