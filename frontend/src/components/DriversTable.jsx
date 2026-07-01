import React from "react";

const DriversTable = ({ drivers }) => (
  <table>
    <thead>
      <tr>
        <th>Водій</th>
        <th>Номер</th>
        <th>Поїздок</th>
        <th>Останній маршрут</th>
      </tr>
    </thead>
    <tbody>
      {drivers.map((driver) => {
        const latestTrip = [...driver.trips].sort((a, b) => (a.created_at < b.created_at ? 1 : -1))[0];
        return (
          <tr key={driver.id}>
            <td>{driver.name}</td>
            <td>{driver.phone_number}</td>
            <td>{driver.trips.length}</td>
            <td>{latestTrip ? latestTrip.route : "—"}</td>
          </tr>
        );
      })}
    </tbody>
  </table>
);

export default DriversTable;
