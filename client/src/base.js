import axios from "axios";

const url = "http://127.0.0.1:8000/";

let settings = {
  baseURL: url
};

if (localStorage.getItem("token")) {
  settings = {
    baseURL: url,
    headers: { token: localStorage.getItem("token") }
  };
}
export const axiosInstance = axios.create(settings);