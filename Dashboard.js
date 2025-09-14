import React, { useEffect, useState } from 'react';


export default function Dashboard() {
const [status, setStatus] = useState({ green_signal: 'N/A', traffic: { NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0 } });


useEffect(() => {
let mounted = true;
async function fetchStatus() {
try {
const res = await fetch('http://localhost:5000/get_status');
if (!res.ok) throw new Error('Network error');
const data = await res.json();
if (mounted) setStatus(data);
} catch (e) {
console.error('Fetch status error', e);
}
}
fetchStatus();
const id = setInterval(fetchStatus, 2000);
return () => { mounted = false; clearInterval(id); };
}, []);


const t = status.traffic || {};


return (
<div style={{ padding: 24, fontFamily: 'Segoe UI, Roboto, Arial' }}>
<h1>🚦 Smart Traffic Dashboard</h1>
<h2>Current Green Signal: <span style={{ color: 'green' }}>{status.green_signal}</span></h2>


<div style={{ display: 'flex', gap: 24, marginTop: 20 }}>
{['NORTH','EAST','SOUTH','WEST'].map(dir => (
<div key={dir} style={{ border: '1px solid #ddd', padding: 12, borderRadius: 8, minWidth: 140 }}>
<h3>{dir}</h3>
<p style={{ fontSize: 22, fontWeight: 'bold' }}>{t[dir] ?? 0}</p>
<div style={{ height: 8, background: '#eee', borderRadius: 4 }}>
<div style={{ height: 8, width: `${Math.min(100, (t[dir] ?? 0) * 2)}%`, background: dir === status.green_signal ? '#32CD32' : '#888', borderRadius: 4 }} />
</div>
</div>
))}
</div>


<p style={{ marginTop: 20, color: '#666' }}>Data refreshes every 2 seconds. Use keyboard <code>q</code> to quit camera windows.</p>
</div>
);
}