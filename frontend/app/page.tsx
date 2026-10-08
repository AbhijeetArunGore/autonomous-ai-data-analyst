'use client';

import React, { useState } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, PointElement, LineElement } from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend);

export default function Home() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'workspace' | 'lineage'>('dashboard');
  const [businessGoal, setBusinessGoal] = useState('Analyze sales performance and identify key retention levers to improve top-line revenue');
  const [preset, setPreset] = useState('');
  const [costTier, setCostTier] = useState('balanced');
  const [status, setStatus] = useState('IDLE');
  const [invalidatedMsg, setInvalidatedMsg] = useState<string | null>(null);
  
  // Mock/Live DAG Nodes
  const [nodes, setNodes] = useState<{ [key: string]: { name: string; status: string; agent: string } }>({
    intake: { name: 'Data Intake', status: 'VALID', agent: 'DataIntakeAgent' },
    profiling: { name: 'Profiling', status: 'VALID', agent: 'DataProfilingAgent' },
    research: { name: 'Research', status: 'VALID', agent: 'ResearcherAgent' },
    plan: { name: 'Plan', status: 'VALID', agent: 'PlannerAgent' },
    quality: { name: 'Data Quality', status: 'VALID', agent: 'DataQualityAgent' },
    imputation: { name: 'Imputation', status: 'VALID', agent: 'MissingValueAgent' },
    features: { name: 'Features', status: 'VALID', agent: 'FeatureEngineeringAgent' },
    kpis: { name: 'KPI Discovery', status: 'VALID', agent: 'KPIDiscoveryAgent' },
    statistics: { name: 'Statistics', status: 'VALID', agent: 'StatisticalAnalysisAgent' },
    ml: { name: 'Machine Learning', status: 'VALID', agent: 'MLEngine' },
    anomaly: { name: 'Anomalies', status: 'VALID', agent: 'AnomalyDetectionEngine' },
    segmentation: { name: 'Segmentation', status: 'VALID', agent: 'SegmentationEngine' },
    visualizations: { name: 'Visualizations', status: 'VALID', agent: 'VisualizationAgent' },
    validation: { name: 'Validation', status: 'VALID', agent: 'ValidationAgent' },
    insights: { name: 'Insights', status: 'VALID', agent: 'InsightAgent' },
    recommendations: { name: 'Recommendations', status: 'VALID', agent: 'ConsultingAgent' },
    storytelling: { name: 'Storytelling', status: 'VALID', agent: 'StorytellingAgent' },
  });

  const [selectedImputation, setSelectedImputation] = useState('median');

  // Handle Preset change
  const handlePresetChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    setPreset(val);
    if (val === 'sales') {
      setBusinessGoal('Analyze why sales declined in Q3 and identify actions to increase revenue');
    } else if (val === 'churn') {
      setBusinessGoal('Identify customers at high risk of churn and explain strongest drivers');
    } else if (val === 'fraud') {
      setBusinessGoal('Isolate high-risk suspicious transaction patterns and minimize false positives');
    } else if (val === 'marketing') {
      setBusinessGoal('Optimize marketing campaign ROI across acquisition channels');
    }
  };

  // Run Analysis Simulation/Live Execution
  const runAnalysis = () => {
    setStatus('RUNNING');
    setActiveTab('workspace');
    setInvalidatedMsg(null);
    
    // Animate node execution state
    let count = 0;
    const nodeKeys = Object.keys(nodes);
    const interval = setInterval(() => {
      if (count < nodeKeys.length) {
        const key = nodeKeys[count];
        setNodes(prev => ({
          ...prev,
          [key]: { ...prev[key], status: 'VALID' }
        }));
        count++;
      } else {
        clearInterval(interval);
        setStatus('COMPLETED');
      }
    }, 150);
  };

  // Analyst HITL Intervention: Change Imputation Strategy
  const handleImputationChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newVal = e.target.value;
    setSelectedImputation(newVal);
    
    // Downstream Invalidation Transitive Closure
    const invalidatedKeys = ['imputation', 'features', 'kpis', 'statistics', 'ml', 'anomaly', 'segmentation', 'visualizations', 'validation', 'insights', 'recommendations', 'storytelling'];
    
    setNodes(prev => {
      const copy = { ...prev };
      invalidatedKeys.forEach(k => {
        copy[k] = { ...copy[k], status: 'INVALIDATED' };
      });
      return copy;
    });

    setInvalidatedMsg(`Analyst changed Missing Value Strategy from 'median' to '${newVal}'. 12 downstream nodes invalidated.`);
  };

  // Audio Speech Synthesis Narration
  const speakBriefing = () => {
    if ('speechSynthesis' in window) {
      const text = "Welcome to your AI Data Analyst executive briefing. Our multi-agent analysis reveals that early-lifecycle customer retention is the primary driver of revenue performance. Implementing targeted onboarding campaigns for high-risk accounts will deliver significant ROI.";
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      window.speechSynthesis.speak(utterance);
    } else {
      alert("Audio synthesis supported on browser window.");
    }
  };

  const chartData = {
    labels: ['Electronics', 'Apparel', 'Home Goods', 'Services', 'Software'],
    datasets: [
      {
        label: 'Average Revenue ($)',
        data: [985, 420, 310, 650, 1120],
        backgroundColor: 'rgba(99, 102, 241, 0.6)',
        borderColor: '#6366f1',
        borderWidth: 1,
      },
    ],
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* Header Navbar */}
      <header className="navbar">
        <div className="brand">
          <span className="brand-badge">⚡ AI DATA ANALYST OS</span>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', fontWeight: 500 }}>v0.1.0 Next.js App</span>
        </div>
        <div className="nav-links">
          <button className={`nav-btn ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>Dashboard</button>
          <button className={`nav-btn ${activeTab === 'workspace' ? 'active' : ''}`} onClick={() => setActiveTab('workspace')}>Analysis Workspace</button>
          <button className={`nav-btn ${activeTab === 'lineage' ? 'active' : ''}`} onClick={() => setActiveTab('lineage')}>Lineage & Audit</button>
        </div>
      </header>

      {/* Main Container */}
      <main className="container">
        
        {/* TAB 1: DASHBOARD */}
        {activeTab === 'dashboard' && (
          <section>
            <div className="hero">
              <div className="card">
                <div className="card-title">
                  <span>🚀 Start Autonomous Analysis</span>
                  <span style={{ fontSize: '0.8rem', color: 'var(--accent-cyan)' }}>Multi-Agent Graph</span>
                </div>
                
                <div className="form-group">
                  <label className="form-label">Upload Dataset (CSV / Excel)</label>
                  <input type="file" className="form-input" accept=".csv,.xlsx,.xls" />
                </div>

                <div className="form-group">
                  <label className="form-label">Natural Language Business Objective</label>
                  <textarea 
                    className="form-textarea" 
                    rows={3} 
                    value={businessGoal} 
                    onChange={e => setBusinessGoal(e.target.value)}
                  />
                </div>

                <div className="form-group" style={{ display: 'flex', gap: '1rem' }}>
                  <div style={{ flex: 1 }}>
                    <label className="form-label">Cost / Performance Tier</label>
                    <select className="form-select" value={costTier} onChange={e => setCostTier(e.target.value)}>
                      <option value="balanced">Balanced (Default)</option>
                      <option value="economy">Economy (Low Cost)</option>
                      <option value="quality">Quality (Deep Reasoning)</option>
                    </select>
                  </div>
                  <div style={{ flex: 1 }}>
                    <label className="form-label">Demo Preset Scenario</label>
                    <select className="form-select" value={preset} onChange={handlePresetChange}>
                      <option value="">-- Select Scenario --</option>
                      <option value="sales">Retail Sales Analysis</option>
                      <option value="churn">Customer Churn Prediction</option>
                      <option value="fraud">Fraud Transaction Isolation</option>
                      <option value="marketing">Marketing Campaign ROI</option>
                    </select>
                  </div>
                </div>

                <button className="btn-primary" onClick={runAnalysis}>
                  Run Autonomous Analysis Graph →
                </button>
              </div>

              <div className="card">
                <div className="card-title">
                  <span>📊 System Telemetry</span>
                  <span style={{ fontSize: '0.8rem', color: 'var(--accent-green)' }}>Active</span>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Registered Agents</span>
                    <span style={{ fontWeight: 700, color: 'var(--accent-cyan)' }}>17 Specialized Agents</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Analytical Engines</span>
                    <span style={{ fontWeight: 700, color: '#fff' }}>Polars / SciPy / Sklearn</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Validation Pass Rate</span>
                    <span style={{ fontWeight: 700, color: 'var(--accent-green)' }}>100% Verified</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Orchestration Model</span>
                    <span style={{ fontWeight: 700, color: 'var(--primary)' }}>Analytical DAG</span>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* TAB 2: WORKSPACE */}
        {activeTab === 'workspace' && (
          <section>
            
            {/* Audio Executive Briefing Banner */}
            <div className="audio-widget">
              <div>
                <h4 style={{ color: '#fff', marginBottom: '0.25rem' }}>Executive Briefing & Audio Narration</h4>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Click below to play executive audio narration script.</p>
              </div>
              <button className="audio-btn" onClick={speakBriefing}>
                <span>🔊</span> Listen to Narration
              </button>
            </div>

            {/* Human In The Loop Invalidation Banner */}
            {invalidatedMsg && (
              <div style={{ background: 'rgba(245, 158, 11, 0.15)', border: '1px solid var(--accent-amber)', padding: '1rem', borderRadius: '8px', marginBottom: '1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <strong style={{ color: 'var(--accent-amber)' }}>Human-In-The-Loop Decision Changed</strong>
                    <p style={{ fontSize: '0.85rem', color: '#fff', marginTop: '0.25rem' }}>{invalidatedMsg}</p>
                  </div>
                  <button style={{ background: 'var(--accent-amber)', border: 'none', color: '#000', fontWeight: 700, padding: '0.5rem 1rem', borderRadius: '6px', cursor: 'pointer' }} onClick={runAnalysis}>
                    Re-run Affected Nodes →
                  </button>
                </div>
              </div>
            )}

            {/* DAG Graph Workspace & HITL Controls */}
            <div className="card" style={{ marginBottom: '2rem' }}>
              <div className="card-title">
                <span>🧠 Analytical Dependency Graph (DAG) Workspace</span>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                  <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>HITL Imputation Strategy:</label>
                  <select className="form-select" style={{ padding: '0.25rem 0.5rem', width: 'auto' }} value={selectedImputation} onChange={handleImputationChange}>
                    <option value="median">Median (Default)</option>
                    <option value="mean">Mean</option>
                    <option value="mode">Mode</option>
                    <option value="knn">KNN Imputation</option>
                    <option value="drop">Drop Rows</option>
                  </select>
                  <span style={{ fontSize: '0.8rem', background: 'rgba(16, 185, 129, 0.2)', color: 'var(--accent-green)', padding: '0.25rem 0.5rem', borderRadius: '4px' }}>{status}</span>
                </div>
              </div>

              <div className="dag-grid">
                {Object.entries(nodes).map(([key, node]) => (
                  <div key={key} className={`dag-node status-${node.status}`}>
                    <div className="node-name">{node.name}</div>
                    <div className="node-status">{node.status}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* KPI Cards */}
            <h3 style={{ marginBottom: '1rem', color: '#fff' }}>Key Performance Indicators (KPIs)</h3>
            <div className="kpi-grid">
              <div className="kpi-card">
                <div className="kpi-label">Total Aggregate Revenue</div>
                <div className="kpi-value">$1,248,500</div>
                <div className="kpi-sub">↑ 4.2% vs previous period</div>
              </div>
              <div className="kpi-card">
                <div className="kpi-label">Average Order Value (AOV)</div>
                <div className="kpi-value">$342.80</div>
                <div className="kpi-sub">↑ 1.8% average basket size</div>
              </div>
              <div className="kpi-card">
                <div className="kpi-label">Customer Retention Rate</div>
                <div className="kpi-value">86.3%</div>
                <div className="kpi-sub">↓ 2.1% SMB segment drop-off</div>
              </div>
              <div className="kpi-card">
                <div className="kpi-label">Churn Rate</div>
                <div className="kpi-value">13.7%</div>
                <div className="kpi-sub">Concentrated in first 90 days</div>
              </div>
            </div>

            {/* Chart Visualization */}
            <div className="card" style={{ marginBottom: '2rem' }}>
              <div className="card-title">
                <span>📈 Category Revenue Bar Chart</span>
              </div>
              <div style={{ height: '300px' }}>
                <Bar data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
              </div>
            </div>

            {/* Insights and Recommendations */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
              <div className="card">
                <div className="card-title">
                  <span>💡 Evidence-Grounded Insights</span>
                </div>
                <div className="insight-card">
                  <div style={{ fontWeight: 600, color: '#fff', marginBottom: '0.25rem' }}>Primary Retention Drop-off in First 90 Days</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--accent-cyan)', background: 'rgba(6, 182, 212, 0.1)', padding: '0.25rem 0.5rem', borderRadius: '4px', display: 'inline-block', marginBottom: '0.5rem' }}>
                    Evidence: Welch's t-test p = 0.002, d = 0.74
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    Customer churn in the SMB segment reaches 17.6% during the first 90 days compared to 7.8% in Enterprise accounts. Early onboarding engagement is the primary predictor.
                  </p>
                </div>
              </div>

              <div className="card">
                <div className="card-title">
                  <span>🎯 Actionable Recommendations</span>
                </div>
                <div style={{ background: 'rgba(18, 26, 44, 0.8)', borderLeft: '4px solid var(--accent-green)', padding: '1.25rem', borderRadius: '8px' }}>
                  <div style={{ fontWeight: 600, color: '#fff', marginBottom: '0.25rem' }}>Launch Automated Onboarding Sequence</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--accent-green)', marginBottom: '0.5rem' }}>Priority: High | Impact: High | Effort: Low</div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    Implement product walk-through triggers and success check-ins during days 1-30 to increase adoption and reduce early retention drop-off.
                  </p>
                </div>
              </div>
            </div>

          </section>
        )}

        {/* TAB 3: LINEAGE */}
        {activeTab === 'lineage' && (
          <section>
            <div className="card">
              <div className="card-title">
                <span>📜 End-to-End Lineage & Decision Register</span>
              </div>
              <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: 'var(--accent-cyan)', fontFamily: 'monospace' }}>
                <p>Dataset Hash: sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</p>
                <p>Pipeline Version: v0.1.0-DAG</p>
                <p style={{ marginTop: '1rem', color: '#fff' }}>Decision Audit Log:</p>
                <ul style={{ paddingLeft: '1.5rem', marginTop: '0.5rem', color: 'var(--text-muted)' }}>
                  <li>[2026-10-08 12:30:00] Missing Value Strategy: Default set to 'median' by Profiling Agent</li>
                  {selectedImputation !== 'median' && (
                    <li style={{ color: 'var(--accent-amber)' }}>
                      [2026-10-08 12:35:00] Analyst Intervention: Changed Missing Value Strategy from 'median' to '{selectedImputation}'. Downstream nodes invalidated.
                    </li>
                  )}
                </ul>
              </div>
            </div>
          </section>
        )}

      </main>
    </div>
  );
}
