import React from 'react';

interface AIScoreGaugeProps {
  score: number; // 0-100
  verdict: string;
  confidence: string;
}

export default function AIScoreGauge({ score, verdict, confidence }: AIScoreGaugeProps) {
  const radius = 80;
  const strokeWidth = 16;
  const normalizedRadius = radius - strokeWidth / 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const halfCircumference = circumference / 2;
  const strokeDashoffset = halfCircumference - (score / 100) * halfCircumference;

  let color = 'var(--success-color)';
  if (score > 30 && score <= 60) {
    color = '#eab308'; // yellow
  } else if (score > 60) {
    color = '#ef4444'; // red
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '2rem 0' }}>
      <div style={{ position: 'relative', width: '200px', height: '110px' }}>
        <svg height="110" width="200" style={{ transform: 'rotate(-180deg)' }}>
          {/* Background Arc */}
          <circle
            stroke="var(--border-color)"
            fill="transparent"
            strokeWidth={strokeWidth}
            strokeDasharray={`${halfCircumference} ${circumference}`}
            style={{ strokeLinecap: 'round' }}
            r={normalizedRadius}
            cx="100"
            cy="100"
          />
          {/* Foreground Arc */}
          <circle
            stroke={color}
            fill="transparent"
            strokeWidth={strokeWidth}
            strokeDasharray={`${halfCircumference} ${circumference}`}
            style={{ 
              strokeDashoffset, 
              strokeLinecap: 'round', 
              transition: 'stroke-dashoffset 1s ease-out, stroke 1s ease-out' 
            }}
            r={normalizedRadius}
            cx="100"
            cy="100"
          />
        </svg>
        <div style={{
          position: 'absolute',
          bottom: '10px',
          left: '0',
          right: '0',
          textAlign: 'center',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <span style={{ fontSize: '2.5rem', fontWeight: 'bold', color: 'var(--text-main)', lineHeight: '1' }}>
            {score}%
          </span>
        </div>
      </div>
      
      <div style={{ textAlign: 'center', marginTop: '0.5rem' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-main)', margin: '0 0 0.25rem 0' }}>
          {verdict}
        </h3>
        <span style={{ 
          fontSize: '0.875rem', 
          color: 'var(--text-muted)', 
          backgroundColor: 'var(--card-bg)',
          padding: '2px 8px',
          borderRadius: '12px',
          border: '1px solid var(--border-color)'
        }}>
          {confidence}
        </span>
      </div>
    </div>
  );
}
