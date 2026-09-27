import 'html-midi-player';
import { useState } from 'react';
import { Midi } from '@tonejs/midi';
import * as Tone from 'tone';
import './PlayerControls.css';

function audioBufferToWav(buffer) {
  const numChannels = buffer.numberOfChannels;
  const sampleRate = buffer.sampleRate;
  const length = buffer.length * numChannels * 2 + 44;
  const arrayBuffer = new ArrayBuffer(length);
  const view = new DataView(arrayBuffer);

  function writeString(offset, str) {
    for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
  }

  writeString(0, 'RIFF');
  view.setUint32(4, length - 8, true);
  writeString(8, 'WAVE');
  writeString(12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * numChannels * 2, true);
  view.setUint16(32, numChannels * 2, true);
  view.setUint16(34, 16, true);
  writeString(36, 'data');
  view.setUint32(40, length - 44, true);

  let offset = 44;
  for (let i = 0; i < buffer.length; i++) {
    for (let ch = 0; ch < numChannels; ch++) {
      const sample = Math.max(-1, Math.min(1, buffer.getChannelData(ch)[i]));
      view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
      offset += 2;
    }
  }

  return new Blob([arrayBuffer], { type: 'audio/wav' });
}

function PlayerControls({ midiUrl }) {
  const [rendering, setRendering] = useState(false);

  if (!midiUrl) return null;

  const downloadAudio = async () => {
    setRendering(true);
    try {
      const res = await fetch(midiUrl);
      const arrayBuffer = await res.arrayBuffer();
      const midi = new Midi(arrayBuffer);
      const duration = midi.duration + 1;

      const rendered = await Tone.Offline(() => {
        const synth = new Tone.PolySynth(Tone.Synth).toDestination();
        midi.tracks.forEach((track) => {
          track.notes.forEach((note) => {
            synth.triggerAttackRelease(note.name, note.duration, note.time, note.velocity);
          });
        });
      }, duration);

      const wavBlob = audioBufferToWav(rendered.get());
      const url = URL.createObjectURL(wavBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'generated-music.wav';
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Audio render failed:', err);
    } finally {
      setRendering(false);
    }
  };

  return (
    <div className="panel player-panel" style={{ padding: '1rem' }}>
      <midi-player src={midiUrl} sound-font visualizer="#pianoRoll" style={{ width: '100%' }}></midi-player>
      <midi-visualizer id="pianoRoll" type="piano-roll" src={midiUrl} style={{ width: '100%', marginTop: '1rem' }}></midi-visualizer>
      <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1rem' }}>
        <a href={midiUrl} download className="btn-primary" style={{ textDecoration: 'none', flex: 1, textAlign: 'center' }}>
          Download MIDI
        </a>
        <button onClick={downloadAudio} disabled={rendering} className="btn-primary" style={{ flex: 1 }}>
          {rendering ? 'Rendering…' : 'Download Audio (WAV)'}
        </button>
      </div>
    </div>
  );
}

export default PlayerControls;