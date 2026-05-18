import {
  BrowserRouter as Router,
  Routes,
  Route,
  Outlet,
  useLocation,
} from "react-router-dom";
import { useEffect } from "react";
import Map from "./map/Map";
import Home from "./home/Home";
import FooterSection from "./footer/Footer";
import Navbar from "./navbar/Navbar";
import PlanJourney from "./plan/PlanJourney";
import Itinerary from "./itinerary/Itinerary";
import Login from "./login/Login";
import Register from "./register/Register";
import Profile from "./profile/Profile";

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}

function MainLayout() {
  return (
    <div className="app-container">
      <Navbar />
      <main className="main-content">
        <Outlet />
      </main>
      <FooterSection />
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <ScrollToTop />
      <Routes>
        {/* Pages with Navbar and Footer */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/plan" element={<PlanJourney />} />
          <Route path="/itinerary" element={<Itinerary startingHotel={1} destinationHotel={1} landmarkIDs={[1, 24, 31, 51, 10, 8, 23, 42, 37, 16, 12, 40, 21, 9, 45]} />} />
          <Route path="/profile" element={<Profile />} />
        </Route>
        <Route path="/map" element={<Map />} />
        {/* Pages without Navbar and Footer */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}
