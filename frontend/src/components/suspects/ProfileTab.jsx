import { MapPin, Phone, User, Hash, AlertTriangle } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function ProfileTab({ suspect }) {
  const { lang } = useLanguage()
  return (
    <div className="profile-tab">
      <div className="profile-grid">
        <div className="profile-section">
          <h4 className="profile-section-title">{t('personal_information', lang) || "Personal Information"}</h4>
          <div className="profile-info-list">
            <div className="profile-info-row">
              <User size={14} />
              <span className="profile-info-label">{t('full_name', lang) || "Full Name"}</span>
              <span className="profile-info-value">{suspect.name}</span>
            </div>
            <div className="profile-info-row">
              <Hash size={14} />
              <span className="profile-info-label">{t('age', lang) || "Age"}</span>
              <span className="profile-info-value">{suspect.age} {t('years', lang) || "years"}</span>
            </div>
            <div className="profile-info-row">
              <MapPin size={14} />
              <span className="profile-info-label">{t('district', lang) || "District"}</span>
              <span className="profile-info-value">{suspect.district}</span>
            </div>
            <div className="profile-info-row">
              <Phone size={14} />
              <span className="profile-info-label">{t('phone', lang) || "Phone"}</span>
              <span className="profile-info-value">{suspect.phone}</span>
            </div>
          </div>
        </div>

        <div className="profile-section">
          <h4 className="profile-section-title">{t('known_aliases', lang) || "Known Aliases"}</h4>
          <div className="profile-tags">
            {suspect.aliases.map((alias, i) => (
              <span key={i} className="profile-tag">{alias}</span>
            ))}
          </div>
        </div>

        <div className="profile-section">
          <h4 className="profile-section-title">{t('address', lang) || "Address"}</h4>
          <p className="profile-address">{suspect.address}</p>
        </div>

        <div className="profile-section full-width">
          <h4 className="profile-section-title">{t('physical_description', lang) || "Physical Description"}</h4>
          <p className="profile-description">{suspect.physicalDescription}</p>
        </div>

        <div className="profile-section full-width">
          <h4 className="profile-section-title">{t('criminal_summary', lang) || "Criminal Summary"}</h4>
          <p className="profile-description">{suspect.description}</p>
        </div>
      </div>
    </div>
  )
}
