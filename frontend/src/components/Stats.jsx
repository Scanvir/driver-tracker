import React from "react";

const Stats = ({ stats }) => (
  <div className="stats-grid">
    <div className="card">
      <h3>Водії</h3>
      <p>{stats.total_drivers}</p>
    </div>
    <div className="card">
      <h3>Поїздки</h3>
      <p>{stats.total_trips}</p>
    </div>
  </div>
);

export default Stats;
