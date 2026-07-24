import { useEffect, useState } from 'react'
import { useLanguage } from '../../context/LanguageContext'
import { getCountsByDistrict } from '../../services/analyticsLive'

export default function DistrictRanking() {
  const { t } = useLanguage()
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const res = await getCountsByDistrict()
        const list = Array.isArray(res?.data) ? res.data : []
        const sum = list.reduce((s, r) => s + (r.value || 0), 0)
        const mapped = list
          .filter((r) => (r.value || 0) > 0)
          .slice(0, 8)
          .map((r) => ({
            district: r.key || 'Other',
            cases: r.value || 0,
            percentage: sum ? Math.round(((r.value || 0) / sum) * 1000) / 10 : 0,
          }))
        if (!cancelled) setRows(mapped)
      } catch (e) {
        console.error(e)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  return (
    <div className="analytics-district-card">
      <div className="analytics-district-header">
        <h3>{t('Top Districts')}</h3>
        <span className="analytics-district-subtitle">{t('by case count')}</span>
      </div>

      <div className="analytics-district-list">
        {loading ? (
          <p className="text-sm text-slate-400 m-0">{t('Loading...')}</p>
        ) : rows.length === 0 ? (
          <p className="text-sm text-slate-400 m-0">{t('No district data')}</p>
        ) : rows.map((d, i) => (
          <div key={i} className="district-item">
            <div className="district-item-left">
              <span className="district-flag">📍</span>
              <span className="district-name">{t(d.district)}</span>
            </div>
            <div className="district-item-right">
              <span className="district-percentage">{d.percentage}%</span>
              <span className="district-cases">{d.cases.toLocaleString()} {t('cases')}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
