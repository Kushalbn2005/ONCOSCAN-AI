import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import UploadSection from './components/UploadSection';
import ScanStudio from './components/ScanStudio';
import DiagnosisPanel from './components/DiagnosisPanel';
import ModelInfoModal from './components/ModelInfoModal';
import { AlertCircle } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

export default function App() {
  const [rawImageSrc, setRawImageSrc] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);

  // Check Backend Health on Mount
  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/health`);
      if (res.ok) {
        const data = await res.json();
        setIsConnected(data.model_loaded);
      } else {
        setIsConnected(false);
      }
    } catch {
      setIsConnected(false);
    }
  };

  const handleFileSelect = async (file) => {
    setErrorMsg(null);
    setIsLoading(true);

    // Render local preview of raw image
    const reader = new FileReader();
    reader.onload = (e) => {
      setRawImageSrc(e.target.result);
    };
    reader.readAsDataURL(file);

    // Call FastAPI Backend /predict endpoint
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({ detail: 'API Error' }));
        throw new Error(errData.detail || 'Prediction failed');
      }

      const result = await response.json();
      setPredictionData(result);
      setIsConnected(true);
    } catch (err) {
      console.error('Prediction API Error:', err);
      setErrorMsg(err.message || 'Failed to connect to OncoScan AI FastAPI backend at localhost:8000');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setRawImageSrc(null);
    setPredictionData(null);
    setErrorMsg(null);
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '24px 16px' }}>
      
      {/* Header */}
      <Header
        isConnected={isConnected}
        onOpenInfo={() => setIsInfoModalOpen(true)}
        onReset={handleReset}
      />

      {/* Error Alert */}
      {errorMsg && (
        <div style={{
          background: 'rgba(244, 63, 94, 0.12)',
          border: '1px solid rgba(244, 63, 94, 0.3)',
          color: '#fb7185',
          padding: '14px 20px',
          borderRadius: 'var(--radius-md)',
          marginBottom: '24px',
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          fontSize: '0.88rem'
        }}>
          <AlertCircle size={20} color="var(--status-danger)" />
          <span><strong>Inference Warning:</strong> {errorMsg}</span>
        </div>
      )}

      {/* Main Studio Grid */}
      <main>
        {/* Upload & Preset Sample Bar */}
        <UploadSection onFileSelect={handleFileSelect} isLoading={isLoading} />

        {/* 2-Column Inspection Studio & Diagnostic Results */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(320px, 1fr) minmax(320px, 440px)',
          gap: '24px',
          alignItems: 'stretch'
        }}>
          {/* Left Column: Visual Grad-CAM MRI Viewer */}
          <ScanStudio
            rawImageSrc={rawImageSrc}
            gradcamUrl={predictionData?.gradcam_url}
            isLoading={isLoading}
            baseUrl={API_BASE_URL}
          />

          {/* Right Column: Classification Results & Clinical Summary */}
          <DiagnosisPanel
            predictionData={predictionData}
            isLoading={isLoading}
          />
        </div>
      </main>

      {/* Model Info Modal */}
      <ModelInfoModal
        isOpen={isInfoModalOpen}
        onClose={() => setIsInfoModalOpen(false)}
      />

      {/* Footer */}
      <footer style={{ marginTop: '40px', textAlign: 'center', fontSize: '0.78rem', color: 'var(--text-dim)', borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '20px' }}>
        OncoScan AI Clinical Assistant • Powered by EfficientNetB0 & Grad-CAM Heatmaps • For Investigational & Research Use
      </footer>

    </div>
  );
}
