import axios from "axios";

const url = "http://127.0.0.1:8000/";

let settings = {
  baseURL: url
};

if (localStorage.getItem("access")) {
  settings = {
    baseURL: url,
    headers: {
      Authorization: `Bearer `+ localStorage.getItem("access")
    }
  };
}
export const axiosInstance = axios.create(settings);