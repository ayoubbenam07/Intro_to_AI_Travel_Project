import Map from "./map/Map"
import Home from "./home/Home"
import FooterSection from "./footer/Footer";
import Navbar from "./navbar/Navbar";
import PlanJourney from "./plan/PlanJourney";

export default function App() {

  return <>
    <Navbar />
    {/* <Home /> */}
    <PlanJourney />
    <FooterSection />
  </>;
}
;