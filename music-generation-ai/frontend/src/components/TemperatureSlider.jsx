function TemperatureSlider({ value, onChange }) {
  return (
    <div className="panel" style={{ padding: '1rem' }}>
      <label style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>
        CREATIVITY — {value.toFixed(1)}
      </label>
      <input
        type="range"
        min="0.1"
        max="2.0"
        step="0.1"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={{ width: '100%', accentColor: 'var(--color-crimson-bright)', marginTop: '0.5rem' }}
      />
    </div>
  );
}

export default TemperatureSlider;