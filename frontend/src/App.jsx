import React, { useEffect, useState } from "react";
import { fetchDrivers, fetchStats, syncGoogleForms } from "./api";
import DriversTable from "./components/DriversTable";
import Stats from "./components/Stats";
import "./App.css";

function App() {
  const [drivers, setDrivers] = useState([]);
  const [stats, setStats] = useState({ total_drivers: 0, total_trips: 0 });
  const [loading, setLoading] = useState(true);

  const load = async () => {
    const [driversData, statsData] = await Promise.all([fetchDrivers(), fetchStats()]);
    setDrivers(driversData);
    setStats(statsData);
    setLoading(false);
  };

  useEffect(() => {
    load();
    const timer = setInterval(load, 10000);
    return () => clearInterval(timer);
  }, []);

  const handleSync = async () => {
    await syncGoogleForms();
    await load();
  };

  if (loading) return <div className="container">Loading...</div>;

  return (
    <div className="container">
      <h1>Driver Tracker</h1>
      <button onClick={handleSync}>Sync Google Forms</button>
      <Stats stats={stats} />
      <DriversTable drivers={drivers} />
    </div>
  );
}

export default App;
