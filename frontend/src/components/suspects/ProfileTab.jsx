import { MapPin, Phone, User, Hash, AlertTriangle } from 'lucide-react'

export default function ProfileTab({ suspect }) {
  return (
    <div className="profile-tab">
      <div className="profile-grid">
        <div className="profile-section">
          <h4 className="profile-section-title">Personal Information</h4>
          <div className="profile-info-list">
            <div className="profile-info-row">
              <User size={14} />
              <span className="profile-info-label">Full Name</span>
              <span className="profile-info-value">{suspect.name}</span>
            </div>
            <div className="profile-info-row">
              <Hash size={14} />
              <span className="profile-info-label">Age</span>
              <span className="profile-info-value">{suspect.age} years</span>
            </div>
            <div className="profile-info-row">
              <MapPin size={14} />
              <span className="profile-info-label">District</span>
              <span className="profile-info-value">{suspect.district}</span>
            </div>
            <div className="profile-info-row">
              <Phone size={14} />
              <span className="profile-info-label">Phone</span>
              <span className="profile-info-value">{suspect.phone}</span>
            </div>
          </div>
        </div>

        <div className="profile-section">
          <h4 className="profile-section-title">Known Aliases</h4>
          <div className="profile-tags">
            {suspect.aliases.map((alias, i) => (
              <span key={i} className="profile-tag">{alias}</span>
            ))}
          </div>
        </div>

        <div className="profile-section">
          <h4 className="profile-section-title">Address</h4>
          <p className="profile-address">{suspect.address}</p>
        </div>

        <div className="profile-section full-width">
          <h4 className="profile-section-title">Physical Description</h4>
          <p className="profile-description">{suspect.physicalDescription}</p>
        </div>

        <div className="profile-section full-width">
          <h4 className="profile-section-title">Criminal Summary</h4>
          <p className="profile-description">{suspect.description}</p>
        </div>
      </div>
    </div>
  )
}
