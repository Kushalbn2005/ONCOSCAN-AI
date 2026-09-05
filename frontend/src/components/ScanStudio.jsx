import React, { useState } from 'react';
import { Eye, Layers, Sliders, Maximize2, Download, Flame, Sparkles } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function ScanStudio({
  rawImageSrc,
  gradcamUrl,
  isLoading,
}) {
  const [opacity, setOpacity] = useState(65);
  const [viewMode, setViewMode] = useState('overlay'); // 'overlay', 'side-by-side', 'raw', 'gradcam'

  const fullGradcamUrl = gradcamUrl
    ? (gradcamUrl.startsWith('http')
      ? gradcamUrl
      : `${API_BASE_URL}${gradcamUrl}`)
    : null;

  return (
    <div className="glass-panel" style={{ padding: '24px', height: '100%', display: 'flex', flexDirection: 'column' }}>

      {/* Studio Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '1.1rem', color: '#fff', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Eye size={20} color="var(--primary)" />
            MRI Neural Inspection Studio
          </h2>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: 0 }}>
            Grad-CAM heatmap highlights cerebral regions driving AI model classification
          </p>
        </div>

        {/* View Mode Switcher */}
        <div style={{ display: 'flex', gap: '6px', background: 'rgba(0,0,0,0.3)', padding: '4px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <button
            className={`btn-secondary ${viewMode === 'overlay' ? 'active' : ''}`}
            onClick={() => setViewMode('overlay')}
            style={{ padding: '6px 12px', fontSize: '0.78rem' }}
          >
            <Layers size={14} /> Overlay
          </button>
          <button
            className={`btn-secondary ${viewMode === 'side-by-side' ? 'active' : ''}`}
            onClick={() => setViewMode('side-by-side')}
            style={{ padding: '6px 12px', fontSize: '0.78rem' }}
          >
            Split View
          </button>
          <button
            className={`btn-secondary ${viewMode === 'raw' ? 'active' : ''}`}
            onClick={() => setViewMode('raw')}
            style={{ padding: '6px 12px', fontSize: '0.78rem' }}
          >
            Raw MRI
          </button>
          <button
            className={`btn-secondary ${viewMode === 'gradcam' ? 'active' : ''}`}
            onClick={() => setViewMode('gradcam')}
            style={{ padding: '6px 12px', fontSize: '0.78rem' }}
          >
            Heatmap
          </button>
        </div>
      </div>

      {/* Main Image Viewer Box */}
      <div
        className="medical-viewer"
        style={{
          flex: 1,
          minHeight: '360px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          padding: '16px'
        }}
      >
        {isLoading && <div className="scan-line" />}

        {!rawImageSrc && !isLoading && (
          <div style={{ textAlign: 'center', color: 'var(--text-dim)', padding: '40px' }}>
            <Layers size={48} style={{ opacity: 0.3, marginBottom: '12px' }} />
            <p style={{ fontSize: '0.9rem' }}>No MRI scan loaded.</p>
            <p style={{ fontSize: '0.78rem', marginTop: '4px' }}>Upload an image or pick a clinical sample above to start analysis.</p>
          </div>
        )}

        {rawImageSrc && (
          <div style={{ width: '100%', height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>

            {/* OVERLAY MODE */}
            {viewMode === 'overlay' && (
              <div style={{ position: 'relative', maxWidth: '340px', width: '100%', aspectRatio: '1/1', borderRadius: '12px', overflow: 'hidden', border: '1px solid rgba(255, 255, 255, 0.15)' }}>
                {/* Base Raw Image */}
                <img
                  src={rawImageSrc}
                  alt="Raw MRI Scan"
                  style={{ width: '100%', height: '100%', objectFit: 'contain', display: 'block' }}
                />
                {/* Grad-CAM Heatmap Layer */}
                {fullGradcamUrl && (
                  <img
                    src={fullGradcamUrl}
                    alt="Grad-CAM Overlay"
                    style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      width: '100%',
                      height: '100%',
                      objectFit: 'contain',
                      opacity: opacity / 100,
                      mixBlendMode: 'screen',
                      transition: 'opacity 0.1s linear'
                    }}
                  />
                )}
              </div>
            )}

            {/* SIDE BY SIDE MODE */}
            {viewMode === 'side-by-side' && (
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', width: '100%', maxWidth: '640px' }}>
                <div style={{ textAlign: 'center' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>Original MRI</span>
                  <img src={rawImageSrc} alt="Raw" style={{ width: '100%', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.1)' }} />
                </div>
                <div style={{ textAlign: 'center' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--primary-light)', display: 'block', marginBottom: '6px' }}>Grad-CAM Heatmap</span>
                  {fullGradcamUrl ? (
                    <img src={fullGradcamUrl} alt="Grad-CAM" style={{ width: '100%', borderRadius: '8px', border: '1px solid var(--border-glow)' }} />
                  ) : (
                    <div style={{ padding: '40px', color: 'var(--text-dim)', fontSize: '0.8rem' }}>Generating heatmap...</div>
                  )}
                </div>
              </div>
            )}

            {/* RAW ONLY */}
            {viewMode === 'raw' && (
              <img src={rawImageSrc} alt="Raw MRI" style={{ maxWidth: '340px', width: '100%', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)' }} />
            )}

            {/* GRADCAM ONLY */}
            {viewMode === 'gradcam' && (
              fullGradcamUrl ? (
                <img src={fullGradcamUrl} alt="Grad-CAM" style={{ maxWidth: '340px', width: '100%', borderRadius: '12px', border: '1px solid var(--border-glow)' }} />
              ) : (
                <div style={{ color: 'var(--text-muted)' }}>Generating Grad-CAM visualization...</div>
              )
            )}

          </div>
        )}
      </div>

      {/* Controls & Heatmap Scale Legend */}
      {rawImageSrc && (
        <div style={{ marginTop: '16px', background: 'rgba(0, 0, 0, 0.3)', padding: '14px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>

            {/* Opacity Slider */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flex: 1, minWidth: '200px' }}>
              <Sliders size={16} color="var(--primary)" />
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', minWidth: '100px' }}>
                Heatmap Opacity: <strong style={{ color: '#fff' }}>{opacity}%</strong>
              </span>
              <input
                type="range"
                min="0"
                max="100"
                value={opacity}
                onChange={(e) => setOpacity(Number(e.target.value))}
              />
            </div>

            {/* Heatmap Spectrum Legend */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>Low Focus</span>
              <div style={{
                width: '100px',
                height: '10px',
                borderRadius: '6px',
                background: 'linear-gradient(to right, #0000ff, #00ffff, #00ff00, #ffff00, #ff0000)'
              }} />
              <span style={{ fontSize: '0.72rem', color: 'var(--status-danger)', fontWeight: 600 }}>High Focus</span>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
