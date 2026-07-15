export default function LogoIcon({ size = 32, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <rect x="4" y="4" width="10" height="10" rx="2.5" fill="white" />
      <rect x="18" y="4" width="10" height="10" rx="2.5" fill="white" />
      <rect x="4" y="18" width="10" height="10" rx="2.5" fill="white" />
      <rect x="18" y="18" width="10" height="10" rx="2.5" fill="white" />
    </svg>
  )
}
