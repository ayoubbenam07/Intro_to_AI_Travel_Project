import {
  BrowserRouter as Router,
  Routes,
  Route,
  Outlet,
} from "react-router-dom";
import Map from "./map/Map";
import Home from "./home/Home";
import FooterSection from "./footer/Footer";
import Navbar from "./navbar/Navbar";
import PlanJourney from "./plan/PlanJourney";
import Login from "./login/Login";
import Register from "./register/Register";

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
      <Routes>
        {/* Pages with Navbar and Footer */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/plan" element={<PlanJourney />} />
        </Route>
        <Route path="/map" element={<Map />} />
        {/* Pages without Navbar and Footer */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}
