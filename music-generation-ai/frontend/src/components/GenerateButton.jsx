function GenerateButton({ onClick, loading }) {
  return (
    <button onClick={onClick} disabled={loading} className="btn-primary" style={{ width: '100%', padding: '16px' }}>
      {loading ? 'Generating…' : 'Generate Music'}
    </button>
  );
}

export default GenerateButton;