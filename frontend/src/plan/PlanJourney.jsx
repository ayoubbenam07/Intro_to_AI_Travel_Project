import { useState, useEffect } from "react";
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

import { useNavigate } from "react-router-dom";

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

  function handleGenerate() {
    const formData = {
      budget,
      hotel,
      date,
      startTime: `${String(startHour).padStart(2, "0")}:${String(startMinute).padStart(2, "0")}`,
      landmarkTypes,
      algorithm,
    };
    console.log("🚀 Generate itinerary:", formData);
    navigate("/map");
  }

  return (
    <div className="plan-page-v2">

      {/* ── Hero Banner (Profile-style fade) ── */}
      <section className="plan-hero">
        <img
          src="/images/background_image2.jpg"
          alt="Algiers cityscape"
          className="plan-hero__img"
          loading="eager"
        />
        <div className="plan-hero__gradient" />
        <div className="plan-hero__content">
          <div className="plan-hero__inner">
            <h1 className="plan-hero__title">Plan your Algiers adventure.</h1>
            <p className="plan-hero__subtitle">
              Configure your itinerary in a few steps — our AI will handle the rest.
            </p>
          </div>
        </div>
      </section>

      {/* ── Main Content ── */}
      <main className="plan-main">

        {/* Stepper bar */}
        <div className="plan-stepper-bar">
          <Stepper
            steps={STEPS}
            currentStep={phase}
            onStepClick={(i) => i <= phase && setPhase(i)}
          />
        </div>

        {/* Two-column grid: Form + Companion */}
        <div className="plan-grid">

          {/* Left — Form card */}
          <div className="plan-form-card">
            <div className="plan-form-card__body">
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
                  disabled={!canNext()}
                  onClick={handleGenerate}
                >
                  ✨ Generate Itinerary
                </Button>
              )}
            </div>
          </div>

          {/* Right — Companion card */}
          <div className="plan-companion-wrap">
            <Companion
              phase={phase}
              formData={{ budget, hotel, date, startHour, startMinute, landmarkTypes, algorithm }}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
