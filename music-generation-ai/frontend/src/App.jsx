import { useState } from 'react';
import AnimatedBackground from './components/AnimatedBackground';
import LogoMark from './components/LogoMark';
import SeedPicker from './components/SeedPicker';
import TemperatureSlider from './components/TemperatureSlider';
import LengthControl from './components/LengthControl';
import PlayerControls from './components/PlayerControls';
import { useGenerateMusic } from './hooks/useGenerateMusic';
import './styles/theme.css';

function App() {
  const { seeds, loading, error, resultUrl, generate } = useGenerateMusic();
  const [selectedSeed, setSelectedSeed] = useState('Seed 1');
  const [temperature, setTemperature] = useState(1.0);
  const [numNotes, setNumNotes] = useState(200);

  const handleGenerate = () => {
    generate({ seedName: selectedSeed, numNotes, temperature });
  };

  return (
    <>
      <AnimatedBackground />
      <div style={{ padding: '2rem', maxWidth: '640px', margin: '4rem auto 0', position: 'relative' }}>
        <header style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem', marginBottom: '2.5rem' }}>
          <LogoMark size={56} />
          <h1 style={{ fontSize: '2.25rem', fontWeight: 700, letterSpacing: '0.02em', textAlign: 'center' }}>
            Music Generation AI
          </h1>
        </header>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <SeedPicker seeds={seeds} selected={selectedSeed} onSelect={setSelectedSeed} />
          <TemperatureSlider value={temperature} onChange={setTemperature} />
          <LengthControl value={numNotes} onChange={setNumNotes} />
          <div style={{ textAlign: 'center' }}>
            <button onClick={handleGenerate} disabled={loading} className="btn-primary" style={{ padding: '14px 48px' }}>
              {loading ? 'Generating…' : 'Generate Music'}
            </button>
          </div>
          {error && (
              <div className="panel" style={{ padding: '1rem', borderColor: 'var(--color-crimson-bright)' }}>
                <p style={{ color: 'var(--color-crimson-glow)', margin: 0, fontSize: '0.9rem' }}>
               ⚠ {error}
                </p>
              </div>)
          }
          <PlayerControls midiUrl={resultUrl} />
        </div>
      </div>
    </>
  );
}

export default App;