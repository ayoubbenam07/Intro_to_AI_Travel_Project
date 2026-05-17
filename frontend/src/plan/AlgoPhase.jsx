const ALGORITHMS = [
  { id: "greedy", name: "Greedy", icon: "⚡", desc: "Fast heuristic, picks best next step" },
  { id: "sa", name: "Simulated Annealing", icon: "🌡️", desc: "Probabilistic search with cooling" },
  { id: "ga", name: "Genetic Algorithm", icon: "🧬", desc: "Evolution-inspired optimization" },
  { id: "hc", name: "Hill Climbing", icon: "⛰️", desc: "Iterative local improvement" },
  { id: "abc", name: "Artificial Bee Colony", icon: "🐝", desc: "Swarm intelligence approach" },
  { id: "acs", name: "Ant Colony System", icon: "🐜", desc: "Pheromone-based pathfinding" },
  { id: "csp", name: "CSP", icon: "🧩", desc: "Constraint satisfaction solver" },
  { id: "acs_hybrid", name: "ACS Hybrid", icon: "🔀", desc: "Combined ACS + local search" },
];

/**
 * AlgoPhase — Algorithm selection.
 */
export default function AlgoPhase({ selected, onChange }) {
  return (
    <div className="plan-phase" key="algo">
      <h2 className="plan-phase__heading">Algorithm</h2>
      <p className="plan-phase__desc">
        Choose the AI algorithm that will optimize your itinerary.
      </p>

      <div className="algo-grid">
        {ALGORITHMS.map((algo) => (
          <button
            key={algo.id}
            type="button"
            className={`algo-card ${selected === algo.id ? "algo-card--selected" : ""}`}
            onClick={() => onChange(algo.id)}
          >
            <div className="algo-card__icon">{algo.icon}</div>
            <div className="algo-card__name">{algo.name}</div>
            <div className="algo-card__desc">{algo.desc}</div>
          </button>
        ))}
      </div>
    </div>
  );
}

export { ALGORITHMS };
