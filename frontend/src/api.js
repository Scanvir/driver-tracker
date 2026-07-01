import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchDrivers = async () => {
  const { data } = await api.get("/drivers");
  return data;
};

export const fetchStats = async () => {
  const { data } = await api.get("/drivers/stats/overview");
  return data;
};

export const syncGoogleForms = async () => {
  const { data } = await api.post("/google-forms/sync");
  return data;
};
