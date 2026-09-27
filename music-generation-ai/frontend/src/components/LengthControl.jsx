function LengthControl({ value, onChange }) {
  return (
    <div className="panel" style={{ padding: '1rem' }}>
      <label style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>
        LENGTH — {value} notes
      </label>
      <input
        type="range"
        min="20"
        max="500"
        step="10"
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value))}
        style={{ width: '100%', accentColor: 'var(--color-crimson-bright)', marginTop: '0.5rem' }}
      />
    </div>
  );
}

export default LengthControl;