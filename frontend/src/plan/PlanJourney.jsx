import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./PlanJourney.css";

import Stepper from "../components/Stepper";
import Button from "../components/Button";

import BudgetPhase from "./BudgetPhase";
import HotelPhase from "./HotelPhase";
import DatePhase from "./DatePhase";
import LandmarksPhase, { LANDMARK_TYPES } from "./LandmarksPhase";
import AlgoPhase from "./AlgoPhase";
import Companion from "./Companion";

import { loadHotels } from "../map/data";

const STEPS = [
  { label: "Budget" },
  { label: "Hotel" },
  { label: "Date" },
  { label: "Landmarks" },
  { label: "Algorithm" },
];

export default function PlanJourney() {
  const navigate = useNavigate();
  const [phase, setPhase] = useState(0);
  const [hotels, setHotels] = useState([]);

  // Form state
  const [budget, setBudget] = useState(12);
  const [hotel, setHotel] = useState(null);
  const [date, setDate] = useState("");
  const [startHour, setStartHour] = useState(9);
  const [startMinute, setStartMinute] = useState(0);
  const [landmarkTypes, setLandmarkTypes] = useState(
    LANDMARK_TYPES.map((t) => t.key)
  );
  const [algorithm, setAlgorithm] = useState("");

  // Load hotels once
  useEffect(() => {
    loadHotels().then(setHotels).catch(console.error);
  }, []);

  const canNext = () => {
    switch (phase) {
      case 0: return budget >= 1;
      case 1: return hotel !== null;
      case 2: return date !== "";
      case 3: return landmarkTypes.length > 0;
      case 4: return algorithm !== "";
      default: return false;
    }
  };

  const [isGenerating, setIsGenerating] = useState(false);

  async function handleGenerate() {
    setIsGenerating(true);
    const ALGO_MAP = {
      greedy: "Greedy",
      sa: "SA",
      ga: "GA",
      hc: "HillClimbing",
      abc: "ABC",
      acs: "ACS",
      csp: "CSP",
      acs_hybrid: "ACS_Hybrid",
    };

    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    let dayOfWeekName = "Monday";
    if (date) {
      const dateObj = new Date(date + "T00:00");
      dayOfWeekName = days[dateObj.getDay()];
    }

    const payload = {
      Hotel_Name: hotel.name,
      Travel_day: dayOfWeekName,
      Travel_Time: Number(budget),
      type_filter: landmarkTypes,
      trip_start_time: Number(startHour) + Number(startMinute) / 60,
      algo_name: ALGO_MAP[algorithm] || "Greedy",
    };

    console.log("🚀 Calling solve API with payload:", payload);
    try {
      const token = localStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
      };
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch("http://localhost:8000/api/solve", {
        method: "POST",
        headers: headers,
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to generate itinerary");
      }

      const result = await response.json();
      console.log("✨ Generated itinerary successfully:", result);
      
      // Navigate to /map and pass the generated itinerary
      navigate("/map", { state: { itinerary: result } });
    } catch (err) {
      console.error(err);
      alert(`Error generating itinerary: ${err.message}`);
    } finally {
      setIsGenerating(false);
    }
  }

  return (
    <div className="plan-page">
      {/* Background */}
      <div className="plan-page__bg">
        <img
          src="/images/background_image2.jpg"
          alt="Algiers cityscape"
          loading="eager"
        />
      </div>

      {/* Glass panel */}
      <div className="plan-panel">
        <div className="plan-panel__header">
          <p className="plan-panel__eyebrow">Custom Journey</p>
          <h1 className="plan-panel__title">Plan your Algiers adventure.</h1>
          <p className="plan-panel__subtitle">
            Configure your itinerary in a few steps — our AI will handle the rest.
          </p>

          {/* Stepper */}
          <Stepper
            steps={STEPS}
            currentStep={phase}
            onStepClick={(i) => i <= phase && setPhase(i)}
          />
        </div>

        <div className="plan-panel__content">
          {/* Phase content */}
        {phase === 0 && (
          <BudgetPhase budget={budget} onChange={setBudget} />
        )}
        {phase === 1 && (
          <HotelPhase hotels={hotels} selected={hotel} onChange={setHotel} />
        )}
        {phase === 2 && (
          <DatePhase
            date={date}
            startHour={startHour}
            startMinute={startMinute}
            onDateChange={setDate}
            onHourChange={setStartHour}
            onMinuteChange={setStartMinute}
          />
        )}
        {phase === 3 && (
          <LandmarksPhase
            selectedTypes={landmarkTypes}
            onChange={setLandmarkTypes}
          />
        )}
          {phase === 4 && (
            <AlgoPhase selected={algorithm} onChange={setAlgorithm} />
          )}
        </div>

        {/* Navigation */}
        <div className="plan-nav">
          {phase > 0 ? (
            <Button variant="secondary" onClick={() => setPhase(phase - 1)}>
              ← Back
            </Button>
          ) : (
            <div />
          )}

          {phase < STEPS.length - 1 ? (
            <Button
              variant="primary"
              disabled={!canNext()}
              onClick={() => setPhase(phase + 1)}
            >
              Next →
            </Button>
          ) : (
            <Button
              variant="primary"
              size="lg"
              disabled={!canNext() || isGenerating}
              onClick={handleGenerate}
            >
              {isGenerating ? "⏳ Generating..." : "✨ Generate Itinerary"}
            </Button>
          )}
        </div>
      </div>

      {/* White gradient fade from panel to background */}
      <div className="plan-fade" />

      {/* Right-side contextual companion */}
      <Companion
        phase={phase}
        formData={{ budget, hotel, date, startHour, startMinute, landmarkTypes, algorithm }}
      />
    </div>
  );
}
