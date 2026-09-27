function SeedPicker({ seeds, selected, onSelect }) {
  return (
    <div className="panel" style={{ padding: '1rem' }}>
      <label style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>SEED</label>
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
        {seeds.map((name) => (
          <button
            key={name}
            onClick={() => onSelect(name)}
            className="btn-primary"
            style={{
              padding: '8px 16px',
              opacity: selected === name ? 1 : 0.4,
            }}
          >
            {name}
          </button>
        ))}
      </div>
    </div>
  );
}

export default SeedPicker;