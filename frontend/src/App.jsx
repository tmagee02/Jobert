import { Routes, Route } from "react-router-dom";
import Background from "./components/Background";
import NavBar from "./components/NavBar";
import Home from "./pages/Home.jsx";
import Jobs from "./pages/Jobs.jsx";
import Watchlist from "./pages/Watchlist.jsx";
import About from "./pages/About.jsx";
import JobInfo from "./pages/JobInfo.jsx";
import NotFound from "./pages/NotFound.jsx";

function App() {
  return (
    <div id="app" className="w-full">
      <Background />
      {/* <NavBar /> */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/jobs/:jobId" element={<JobInfo />} />
        <Route path="/watchlist" element={<Watchlist />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}

export default App;
