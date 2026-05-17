import { useMemo, useState, useEffect, useRef } from "react";

/**
 * Companion — Contextual right-side panel that changes per phase.
 */
export default function Companion({ phase, formData }) {
  return (
    <div className="plan-companion">
      {phase === 0 && <BudgetCompanion budget={formData.budget} />}
      {phase === 1 && <HotelCompanion hotel={formData.hotel} />}
      {phase === 2 && <DateCompanion startHour={formData.startHour} />}
      {phase === 3 && <LandmarksCompanion types={formData.landmarkTypes} />}
      {phase === 4 && <AlgoCompanion algorithm={formData.algorithm} />}
    </div>
  );
}

/* ── Phase 0: Budget ── */
function BudgetCompanion({ budget = 12 }) {
  const radius = 100;
  const pathLength = Math.PI * radius; // 314.15
  
  // Budget is 1-24. Percentage is budget/24.
  const percentage = budget / 24;
  const strokeDashoffset = pathLength - (percentage * pathLength);
  
  const nodesCount = Math.floor(budget / 2);
  const maxNodes = 12;
  const nodes = Array.from({ length: maxNodes });
  
  let glowColor = "var(--color-primary)";
  if (budget >= 17) glowColor = "#ff7e5f"; // orange
  else if (budget >= 9) glowColor = "#a18cd1"; // purple

  return (
    <div className="companion-card budget-companion-card" key="budget" style={{ padding: 0, overflow: 'hidden' }}>
      
      {/* Visual Header Inside Card */}
      <div className="budget-visual-header">
        {/* Soft glowing ambient orb in background */}
        <div className="budget-glow-bg" style={{ background: glowColor }} />
        
        <svg viewBox="0 0 280 140" className="budget-arc-svg">
          {/* Background track */}
          <path d={`M 40 120 A ${radius} ${radius} 0 0 1 240 120`} 
                fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="10" strokeLinecap="round" />
          
          {/* Active sweeping track */}
          <path d={`M 40 120 A ${radius} ${radius} 0 0 1 240 120`} 
                fill="none" stroke={glowColor} strokeWidth="10" strokeLinecap="round"
                className="budget-arc-active"
                style={{
                  strokeDasharray: pathLength,
                  strokeDashoffset: strokeDashoffset,
                }} />
          
          {/* Nodes */}
          {nodes.map((_, i) => {
            const nodePercent = (i + 1) / (maxNodes + 1); 
            const angle = Math.PI - (nodePercent * Math.PI);
            const x = 140 + Math.cos(angle) * radius;
            const y = 120 - Math.sin(angle) * radius;
            
            // Only show node if the current budget covers it
            const isActive = budget >= (nodePercent * 24);
            
            return isActive ? (
               <circle key={i} cx={x} cy={y} r="5" fill="#fff" 
                 className="budget-node"
                 style={{
                   animationDelay: `${i * 0.03}s`,
                   filter: `drop-shadow(0 0 6px ${glowColor})`
                 }} />
            ) : null;
          })}
        </svg>

        <div className="budget-center-text">
          <span style={{ fontSize: "36px", fontWeight: "800", color: "#fff", textShadow: `0 0 20px ${glowColor}` }}>{budget}</span>
          <span style={{ fontSize: "12px", textTransform: "uppercase", letterSpacing: "1px", color: "rgba(255,255,255,0.7)", marginTop: "4px" }}>Hours</span>
        </div>
      </div>

      <div className="budget-companion-content" style={{ padding: '32px' }}>
        <div className="companion-card__badge">
          <span className="companion-card__badge-dot" style={{ background: glowColor, transition: "background 0.5s ease" }} />
          Itinerary Maximization
        </div>
        <h3 className="companion-card__title">Time to Explore</h3>
        <p className="companion-card__text">
          {budget < 6 
            ? `With a tight ${budget}-hour window, our AI will prioritize efficiency, maximizing your route to fit as many key landmarks as possible.`
            : budget <= 14
            ? `With a solid ${budget}-hour budget, our AI will maximize your itinerary, packing diverse landmarks into a perfectly optimized route.`
            : `With an expansive ${budget}-hour journey, our AI will unleash its full potential, maximizing your route to hit the maximum number of landmarks across Algiers.`}
        </p>
      </div>
    </div>
  );
}

/* ── Phase 1: Hotel ── */
function HotelCompanion({ hotel }) {
  return (
    <div className="companion-card hotel-companion-card" key="hotel" style={{ padding: 0, overflow: 'hidden' }}>
      {/* Visual Header Inside Card */}
      <div className="hotel-visual-header">
        <div className="map-grid" style={{ animationPlayState: hotel ? 'paused' : 'running' }}></div>
        {!hotel ? (
          <div className="scanning-laser"></div>
        ) : (
          <div className="hotel-pin-drop">
             <div className="radar-ripple r1" />
             <div className="radar-ripple r2" />
             <div className="radar-ripple r3" />
             <div className="radar-pin">📍</div>
          </div>
        )}
      </div>

      <div className="hotel-companion-content" style={{ padding: '32px' }}>
        <div className="companion-card__badge">
          <span className="companion-card__badge-dot" />
          Departure Point
        </div>
        <h3 className="companion-card__title">
          {hotel ? hotel.name : "Choose your base"}
        </h3>
        <p className="companion-card__text">
          {hotel
            ? `Located at ${hotel.latitude.toFixed(4)}°N, ${hotel.longitude.toFixed(4)}°E. The AI will optimize routes starting and ending here.`
            : "Search from 184 hotels across Algiers. Your itinerary starts and ends here."}
        </p>
      </div>
    </div>
  );
}

/* ── Phase 2: Date ── */
function DateCompanion({ startHour = 9 }) {
  const h = Number(startHour);
  
  // Classify time
  const isDawn = h >= 5 && h <= 8;
  const isDay = h >= 9 && h <= 16;
  const isDusk = h >= 17 && h <= 19;
  const isNight = h >= 20 || h <= 4;

  // Determine if it's daytime or nighttime
  const isDaytime = h >= 6 && h <= 18;
  const celestialIcon = isDaytime ? "☀️" : "🌙";

  // Calculate the arc position of the sun/moon
  let progress;
  if (isDaytime) {
    progress = (h - 6) / 12; // 0 to 1
  } else {
    // Night is 18 to 6
    let nightH = h;
    if (nightH < 6) nightH += 24; 
    progress = (nightH - 18) / 12; // 0 to 1
  }

  // Left to right movement (10% to 90%)
  const leftPos = 10 + progress * 80;
  // Arc height (parabola)
  const topPos = 80 - Math.sin(progress * Math.PI) * 50;

  // Text tips
  let tip = "Perfect time for museums and historical sites while everything is open.";
  if (isDawn) tip = "Beat the crowds! Parks and mosques are beautifully quiet in the early hours.";
  if (isDusk) tip = "Enjoy the golden hour. A great time for monuments and public squares.";
  if (isNight) tip = "City lights! Focus on cultural centers, late shopping, and open squares.";

  return (
    <div className="companion-card date-companion-card" key="date" style={{ padding: 0, overflow: 'hidden' }}>
      
      {/* Sky Window Header */}
      <div className="sky-window">
         {/* Background layers for smooth opacity crossfading (CSS gradients can't animate) */}
         <div className="sky-layer dawn" style={{ opacity: isDawn ? 1 : 0 }} />
         <div className="sky-layer day" style={{ opacity: isDay ? 1 : 0 }} />
         <div className="sky-layer dusk" style={{ opacity: isDusk ? 1 : 0 }} />
         <div className="sky-layer night" style={{ opacity: isNight ? 1 : 0 }} />

         {/* Stars if night */}
         <div className="stars-overlay" style={{ opacity: isNight ? 0.5 : 0, transition: 'opacity 1s ease' }} />
         
         {/* The Sun/Moon */}
         <div className="celestial-body" style={{ 
           left: `${leftPos}%`, 
           top: `${topPos}%`, 
           boxShadow: isDaytime ? '0 0 50px 20px rgba(255,255,255,0.4)' : '0 0 20px 10px rgba(255,255,255,0.15)'
         }}>
            {celestialIcon}
         </div>
         
         {/* Parallax Seamless Clouds */}
         <div className="clouds-overlay layer-back"></div>
         <div className="clouds-overlay layer-front"></div>
      </div>

      <div className="date-companion-content" style={{ padding: '32px' }}>
        <div className="companion-card__badge">
          <span className="companion-card__badge-dot" />
          Smart Scheduling
        </div>
        <h3 className="companion-card__title">
          Starting at {String(h).padStart(2, '0')}:00
        </h3>
        <p className="companion-card__text">
          {tip}
        </p>
      </div>
    </div>
  );
}

/* ── Phase 3: Landmarks ── */
const LANDMARK_POSITIONS = [
  { x: 30, y: 50 }, { x: 70, y: 25 }, { x: 120, y: 65 }, { x: 160, y: 35 }, 
  { x: 90, y: 45 }, { x: 50, y: 80 }, { x: 140, y: 20 }, { x: 180, y: 80 }, 
  { x: 20, y: 20 }, { x: 100, y: 85 }, { x: 150, y: 50 }, { x: 60, y: 55 },
  { x: 130, y: 85 }, { x: 40, y: 30 }, { x: 170, y: 60 }, { x: 80, y: 15 },
  { x: 110, y: 30 }, { x: 30, y: 75 }, { x: 190, y: 40 }, { x: 70, y: 65 }
];

function LandmarksCompanion({ types }) {
  const count = types ? types.length : 0;
  
  const activePositions = [];
  for(let i = 0; i < count; i++) {
     activePositions.push(LANDMARK_POSITIONS[i % LANDMARK_POSITIONS.length]);
  }

  return (
    <div className="companion-card landmarks-companion-card" key="landmarks" style={{ padding: 0, overflow: 'hidden' }}>
      
      {/* Visual Header */}
      <div className="algo-visual-header" style={{ position: 'relative' }}>
        
        {count === 0 && (
          <div className="algo-vis-waiting">
            <div className="algo-pulse-grid"></div>
            <div className="algo-waiting-text">Awaiting Input...</div>
          </div>
        )}

        {count > 0 && (
          <div className="algo-vis-landmarks" style={{ position: 'relative', width: '100%', height: '100%' }}>
            
            <svg viewBox="0 0 200 100" className="algo-svg" style={{ zIndex: 2, position: 'relative' }}>
               
               {/* Radar Grid Background */}
               <defs>
                 <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                   <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="0.5"/>
                 </pattern>
                 <linearGradient id="radar-beam" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="rgba(0, 242, 254, 0)" />
                    <stop offset="90%" stopColor="rgba(0, 242, 254, 0.2)" />
                    <stop offset="100%" stopColor="rgba(0, 242, 254, 1)" />
                 </linearGradient>
               </defs>
               <rect width="200" height="100" fill="url(#grid)" />

               {/* SVG Sweeping Radar Beam */}
               <rect x="-20" y="0" width="20" height="100" fill="url(#radar-beam)" className="svg-radar-sweep" />

               {/* Connecting Route Lines */}
               {count > 1 && (
                 <>
                   <polyline 
                     points={activePositions.map(p => `${p.x},${p.y}`).join(' ')} 
                     fill="none" 
                     stroke="rgba(0, 242, 254, 0.2)" 
                     strokeWidth="1.5" 
                     strokeDasharray="4 4"
                   />
                   {/* Traveling data packet */}
                   <polyline 
                     points={activePositions.map(p => `${p.x},${p.y}`).join(' ')} 
                     fill="none" 
                     stroke="#00f2fe" 
                     strokeWidth="2" 
                     className="landmark-route-highlight"
                     style={{ filter: 'drop-shadow(0 0 5px #00f2fe)' }}
                   />
                 </>
               )}

               {/* Landmark Pins */}
               {activePositions.map((pos, i) => {
                 // Beam translates from x=0 to x=220 over 3 seconds.
                 // We subtract 5px so it triggers as the leading edge touches the text box
                 const targetX = Math.max(0, pos.x - 5);
                 const hitTime = (targetX / 220) * 3; 
                 // Negative delay ensures perfect CSS sync starting at frame 0
                 const delay = -(3 - hitTime); 
                 
                 return (
                   <g key={i} className="landmark-pin-group">
                     <circle cx={pos.x} cy={pos.y} r="0" fill="none" stroke="#00f2fe" className="radar-blip-ripple" style={{ animationDelay: `${delay}s` }} />
                     
                     <circle cx={pos.x} cy={pos.y} r="3" fill="#fff" className="radar-blip-core" style={{ animationDelay: `${delay}s` }} />
                     
                     <text x={pos.x} y={pos.y - 6} fill="#fff" fontSize="6" textAnchor="middle" className="radar-blip-text" style={{ animationDelay: `${delay}s`, fontFamily: 'monospace', letterSpacing: '0.5px' }}>
                       {types[i].toUpperCase()}
                     </text>
                   </g>
                 );
               })}
            </svg>
          </div>
        )}

      </div>

      <div className="landmarks-companion-content" style={{ padding: '32px' }}>
        <div className="companion-card__badge">
          <span className="companion-card__badge-dot" />
          Geospatial Radar
        </div>
        <h3 className="companion-card__title">
          {count > 0 ? `${count} ${count === 1 ? "type" : "types"} active` : "Select Landmarks"}
        </h3>
        <p className="companion-card__text">
          {count > 0 
            ? "The AI is scanning the city for these specific categories to build an optimal constellation route."
            : "Choose the types of places you want to visit to begin the scan."}
        </p>
      </div>
    </div>
  );
}

const TYPE_ICONS = {
  Monument: "🏛️", Nature: "🌿", "Historical Site": "🏰",
  Mosque: "🕌", Cathedral: "⛪", Museum: "🎨",
  "Cultural Center & Event Venue": "🎭", Park: "🌳",
  "Public Square": "📍", Beach: "🏖️", "Shopping/Mall": "🛍️",
};

/* ── Phase 4: Algorithm ── */
const ALGO_INFO = {
  greedy:     { name: "Greedy Search", emoji: "⚡", tip: "Fastest execution, picks the highest-rated next stop." },
  sa:         { name: "Simulated Annealing", emoji: "🌡️", tip: "Explores broadly then narrows down — great for balanced routes." },
  ga:         { name: "Genetic Algorithm", emoji: "🧬", tip: "Evolves many candidate routes — best for complex itineraries." },
  hc:         { name: "Hill Climbing", emoji: "⛰️", tip: "Quick iterative improvement — good for shorter budgets." },
  abc:        { name: "Artificial Bee Colony", emoji: "🐝", tip: "Swarm intelligence finds hidden gems other algorithms miss." },
  acs:        { name: "Ant Colony System", emoji: "🐜", tip: "Pheromone-based pathfinding — excels at travel routing." },
  csp:        { name: "Constraint Satisfaction Problem", emoji: "🧩", tip: "Guarantees all constraints are satisfied — no missed windows." },
  acs_hybrid: { name: "Hybrid Ant Colony", emoji: "🔀", tip: "Best of both worlds — ACS global search + local refinement." },
};

function AlgoCompanion({ algorithm }) {
  const info = algorithm ? ALGO_INFO[algorithm] : null;

  return (
    <div className="companion-card algo-companion-card" key="algo" style={{ padding: 0, overflow: 'hidden' }}>
      
      {/* Visual Header */}
      <div className="algo-visual-header">
        
        {!algorithm && (
          <div className="algo-vis-waiting">
            <div className="algo-pulse-grid"></div>
            <div className="algo-waiting-text">Awaiting Input...</div>
          </div>
        )}

        {algorithm === 'greedy' && (
          <div className="algo-vis-greedy">
            <svg viewBox="0 0 200 100" className="algo-svg">
               {/* Background Nodes */}
               <circle cx="20" cy="50" r="3" fill="#fff" opacity="0.3" />
               <circle cx="50" cy="20" r="3" fill="#fff" opacity="0.3" />
               <circle cx="90" cy="40" r="3" fill="#fff" opacity="0.3" />
               <circle cx="120" cy="80" r="3" fill="#fff" opacity="0.3" />
               <circle cx="160" cy="60" r="3" fill="#fff" opacity="0.3" />
               <circle cx="180" cy="20" r="3" fill="#fff" opacity="0.3" />

               {/* Sonar Pings (Evaluating local neighbors) */}
               <circle cx="20" cy="50" r="0" fill="none" stroke="#00f2fe" className="greedy-ping p1" />
               <circle cx="50" cy="20" r="0" fill="none" stroke="#00f2fe" className="greedy-ping p2" />
               <circle cx="90" cy="40" r="0" fill="none" stroke="#00f2fe" className="greedy-ping p3" />
               <circle cx="120" cy="80" r="0" fill="none" stroke="#00f2fe" className="greedy-ping p4" />
               <circle cx="160" cy="60" r="0" fill="none" stroke="#00f2fe" className="greedy-ping p5" />

               {/* Laser Path */}
               <polyline points="20,50 50,20 90,40 120,80 160,60 180,20" fill="none" stroke="#00f2fe" strokeWidth="2" className="greedy-path" />
               
               {/* Actively moving traveler */}
               <circle r="4" fill="#fff" className="greedy-traveler" style={{ filter: 'drop-shadow(0 0 6px #00f2fe)' }} />
            </svg>
          </div>
        )}

        {algorithm === 'hc' && (
          <div className="algo-vis-hc">
            <svg viewBox="0 0 200 100" className="algo-svg">
              {/* Mountain Fill Gradient */}
              <defs>
                 <linearGradient id="hc-grad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="rgba(246, 211, 101, 0.4)" />
                    <stop offset="100%" stopColor="rgba(246, 211, 101, 0)" />
                 </linearGradient>
              </defs>
              <path d="M 0 100 Q 20 50, 40 50 T 80 80 Q 120 20, 160 20 T 200 100 Z" fill="url(#hc-grad)" stroke="none" />
              
              {/* Mountain Outline */}
              <path d="M 0 100 Q 20 50, 40 50 T 80 80 Q 120 20, 160 20 T 200 100" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="2" />
              <path d="M 0 100 Q 20 50, 40 50 T 80 80 Q 120 20, 160 20 T 200 100" fill="none" stroke="#f6d365" strokeWidth="2" className="hc-mountain-line" />

              {/* Climber 1: Gets stuck at local maximum */}
              <circle r="3" fill="#ff416c" className="hc-climber local" style={{ filter: 'drop-shadow(0 0 4px #ff416c)' }} />
              
              {/* Climber 2: Reaches global maximum */}
              <circle r="4" fill="#fff" className="hc-climber global" style={{ filter: 'drop-shadow(0 0 6px #f6d365)' }} />
            </svg>
          </div>
        )}

        {algorithm === 'sa' && (
          <div className="algo-vis-sa">
            <div className="sa-core"></div>
            {[...Array(8)].map((_, i) => (
               <div key={i} className={`sa-atom a${i+1}`}></div>
            ))}
            <svg viewBox="0 0 200 100" className="algo-svg sa-connections">
               {/* Faint crystal bonds that appear only when cold */}
               <polygon points="140,50 128,78 100,90 72,78 60,50 72,22 100,10 128,22" fill="none" stroke="#00f2fe" strokeWidth="1" className="sa-bonds" />
            </svg>
          </div>
        )}

        {algorithm === 'ga' && (
          <div className="algo-vis-ga-3d">
             <div className="dna-strand">
               {[...Array(12)].map((_, i) => (
                  <div key={i} className="dna-rung" style={{ animationDelay: `-${i * 0.25}s` }}>
                     <div className="dna-node top" style={{ animationDelay: `-${i * 0.25}s` }}></div>
                     <div className="dna-node bottom" style={{ animationDelay: `-${i * 0.25}s` }}></div>
                  </div>
               ))}
             </div>
          </div>
        )}

        {algorithm === 'acs' && (
          <div className="algo-vis-acs">
            <svg viewBox="0 0 200 100" className="algo-svg">
              {/* Faint network paths */}
              <g stroke="rgba(255,255,255,0.15)" strokeWidth="1" fill="none">
                 <line x1="20" y1="50" x2="80" y2="20" />
                 <line x1="20" y1="50" x2="80" y2="80" />
                 <line x1="80" y1="20" x2="140" y2="20" />
                 <line x1="80" y1="80" x2="140" y2="80" />
                 <line x1="80" y1="20" x2="180" y2="50" />
                 <line x1="80" y1="80" x2="180" y2="50" />
                 <line x1="140" y1="20" x2="180" y2="50" />
                 <line x1="140" y1="80" x2="180" y2="50" />
              </g>

              {/* Optimal Pheromone Path */}
              <polyline points="20,50 100,50 180,50" fill="none" stroke="#00f2fe" strokeWidth="3" className="acs-optimal-path" style={{ filter: 'drop-shadow(0 0 6px #00f2fe)' }} />
              
              {/* Nodes */}
              <g fill="#fff">
                <circle cx="20" cy="50" r="4" />
                <circle cx="80" cy="20" r="3" />
                <circle cx="80" cy="80" r="3" />
                <circle cx="100" cy="50" r="4" style={{ filter: 'drop-shadow(0 0 6px #00f2fe)' }} />
                <circle cx="140" cy="20" r="3" />
                <circle cx="140" cy="80" r="3" />
                <circle cx="180" cy="50" r="4" />
              </g>

              {/* Ants */}
              <circle r="2.5" fill="#fff" className="acs-ant optimal-1" style={{ filter: 'drop-shadow(0 0 4px #fff)' }} />
              <circle r="2.5" fill="#fff" className="acs-ant optimal-2" style={{ filter: 'drop-shadow(0 0 4px #fff)' }} />
              <circle r="2" fill="rgba(255,255,255,0.6)" className="acs-ant wander-1" />
              <circle r="2" fill="rgba(255,255,255,0.6)" className="acs-ant wander-2" />
            </svg>
          </div>
        )}

        {algorithm === 'acs_hybrid' && (
          <div className="algo-vis-acs-hybrid">
            <svg viewBox="0 0 200 100" className="algo-svg">
              {/* Faint network paths */}
              <g stroke="rgba(255,255,255,0.15)" strokeWidth="1" fill="none">
                 <line x1="20" y1="50" x2="80" y2="20" />
                 <line x1="20" y1="50" x2="80" y2="80" />
                 <line x1="80" y1="20" x2="140" y2="20" />
                 <line x1="80" y1="80" x2="140" y2="80" />
                 <line x1="80" y1="20" x2="180" y2="50" />
                 <line x1="80" y1="80" x2="180" y2="50" />
                 <line x1="140" y1="20" x2="180" y2="50" />
                 <line x1="140" y1="80" x2="180" y2="50" />
              </g>

              {/* Optimal Pheromone Path */}
              <polyline points="20,50 100,50 180,50" fill="none" stroke="#00f2fe" strokeWidth="3" className="acs-optimal-path" style={{ filter: 'drop-shadow(0 0 6px #00f2fe)' }} />
              
              {/* Normal Nodes */}
              <g fill="#fff">
                <circle cx="20" cy="50" r="4" />
                <circle cx="80" cy="20" r="3" />
                <circle cx="80" cy="80" r="3" />
                <circle cx="140" cy="20" r="3" />
                <circle cx="140" cy="80" r="3" />
                <circle cx="180" cy="50" r="4" />
              </g>

              {/* SA Hybrid Engine at the Center */}
              <circle cx="100" cy="50" r="14" className="hybrid-sa-ring r1" />
              <circle cx="100" cy="50" r="22" className="hybrid-sa-ring r2" />
              <circle cx="100" cy="50" r="6" className="hybrid-sa-node" />

              {/* Ants */}
              <circle r="2.5" fill="#fff" className="acs-ant optimal-1" style={{ filter: 'drop-shadow(0 0 4px #fff)' }} />
              <circle r="2.5" fill="#fff" className="acs-ant optimal-2" style={{ filter: 'drop-shadow(0 0 4px #fff)' }} />
              <circle r="2" fill="rgba(255,255,255,0.6)" className="acs-ant wander-1" />
              <circle r="2" fill="rgba(255,255,255,0.6)" className="acs-ant wander-2" />
            </svg>
          </div>
        )}

        {algorithm === 'abc' && (
          <div className="algo-vis-abc">
            <svg viewBox="0 0 200 100" className="algo-svg">
              <defs>
                 {/* Hexagon polygon shape */}
                 <polygon id="hex" points="10,0 20,5 20,15 10,20 0,15 0,5" />
              </defs>
              <g className="honeycomb-group" fill="rgba(246, 211, 101, 0.05)" stroke="#f6d365" strokeWidth="0.5">
                 <use href="#hex" x="80" y="25" className="hex h1" />
                 <use href="#hex" x="102" y="25" className="hex h2" />
                 <use href="#hex" x="69" y="44" className="hex h3" />
                 <use href="#hex" x="91" y="44" className="hex h4" />
                 <use href="#hex" x="113" y="44" className="hex h5" />
                 <use href="#hex" x="80" y="63" className="hex h6" />
                 <use href="#hex" x="102" y="63" className="hex h7" />
              </g>
              
              {/* Bees */}
              <circle r="2.5" fill="#fff" className="bee b1" style={{ filter: 'drop-shadow(0 0 5px #fff)' }}/>
              <circle r="2.5" fill="#fff" className="bee b2" style={{ filter: 'drop-shadow(0 0 5px #fff)' }}/>
              <circle r="2.5" fill="#fff" className="bee b3" style={{ filter: 'drop-shadow(0 0 5px #fff)' }}/>
            </svg>
          </div>
        )}

        {algorithm === 'csp' && (
          <div className="algo-vis-csp">
            <div className="csp-grid">
               {[...Array(9)].map((_, i) => <div key={i} className={`csp-cell c${i+1}`}></div>)}
            </div>
          </div>
        )}

      </div>

      <div className="algo-companion-content" style={{ padding: '32px' }}>
        <div className="companion-card__badge">
          <span className="companion-card__badge-dot" />
          AI Engine
        </div>
        <h3 className="companion-card__title">
          {algorithm ? "Algorithm Ready" : "Pick your optimizer"}
        </h3>
        <p className="companion-card__text">
          {info
            ? info.tip
            : "Each algorithm has different strengths. Choose the one that fits your travel style."}
        </p>
        {info && (
          <div className="companion-hotel" style={{ marginTop: 16 }}>
            <div className="companion-hotel__icon" style={{ fontSize: 22 }}>
              {info.emoji}
            </div>
            <div>
              <div className="companion-hotel__name" style={{ fontWeight: 600 }}>
                {info.name}
              </div>
              <div className="companion-hotel__coords">Ready to calculate optimal route</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
