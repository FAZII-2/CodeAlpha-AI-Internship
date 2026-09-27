import './LogoMark.css';

function LogoMark({ size = 36 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect className="logo-bar" x="6" y="20" width="4" height="8" rx="2"
        fill="var(--color-crimson-glow)" style={{ animationDelay: '0s' }} />
      <rect className="logo-bar" x="14" y="12" width="4" height="24" rx="2"
        fill="var(--color-crimson-bright)" style={{ animationDelay: '0.15s' }} />
      <rect className="logo-bar" x="22" y="4" width="4" height="40" rx="2"
        fill="var(--color-crimson-glow)" style={{ animationDelay: '0.3s' }} />
      <rect className="logo-bar" x="30" y="14" width="4" height="20" rx="2"
        fill="var(--color-crimson-bright)" style={{ animationDelay: '0.45s' }} />
      <rect className="logo-bar" x="38" y="18" width="4" height="12" rx="2"
        fill="var(--color-crimson-glow)" style={{ animationDelay: '0.6s' }} />
    </svg>
  );
}

export default LogoMark;