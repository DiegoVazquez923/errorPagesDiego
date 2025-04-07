import axios from "axios";

//URL de inicio de sesión (JWT)
const API_URL = "http://127.0.0.1:8000/users/token/"
const url = "http://127.0.0.1:8000";

export const login = async (email, password) => {
    try {
      const response = await axios.post(API_URL, { email, password });
      console.log("Login response:", response);
  
      if (response.data.access) {
        // Guardar token y email
        localStorage.setItem("email", email);
        localStorage.setItem("accessToken", response.data.access);
        localStorage.setItem("refreshToken", response.data.refresh);
  
        const users = await axios.get("http://127.0.0.1:8000/users/api/", {
          headers: {
            Authorization: `Bearer ${response.data.access}`,
            "Content-Type": "application/json",
          },
        });
  
        const usuarios = users.data;
        const logueado = usuarios.find((u) => u.email.trim() === email.trim());
  
        if (logueado) {
          localStorage.setItem("userId", logueado.id);
          console.log("Usuario logueado:", logueado);
        } else {
          console.warn("No se encontró un usuario con ese email.");
        }
  
        return response.data;
      }
  
    } catch (error) {
      console.error("Error en login:", error);
      throw error;
    }
  };

export const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    window.location.reload(); // Recargar para actualizar estado
}

export const tokenRefresh = axios.create({
  url,
  timeout: 5000,
  headers: {
    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

tokenRefresh.interceptors.response.use(
  (response) => response,
  async (error) => {
    const peticOrig = error.config;

    if (
      error.response?.status === 401 &&
      !peticOrig._retry &&
      localStorage.getItem("refreshToken")
    ) {
      peticOrig._retry = true;

      try {
        const { data } = await axios.post(`${url}/users/token/refresh/`, {
          refresh: localStorage.getItem("refreshToken"),
        });

        localStorage.setItem("accessToken", data.access);

        tokenRefresh.defaults.headers["Authorization"] = `Bearer ${data.access}`;
        peticOrig.headers["Authorization"] = `Bearer ${data.access}`;

        return tokenRefresh(peticOrig);
      } catch (err) {
        console.error("Error al refrescar token:", err);
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");

        window.location.href = "/login";
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);
