import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const ResetPassword = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:8000/users/reset-password/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ token, password }),
    });

    const data = await response.json();
    if (response.ok) {
        setLoading(false);
      setMessage(data.message);      
      setTimeout(() => navigate("/login"), 2000);
    } else {
        setLoading(false);
      setMessage(data.error);
    }
  };

  if(loading){
    return (
        <div className="d-flex justify-content-center align-items-center vh-100">
          <div className="spinner-border text-primary" style={{ width: "5rem", height: "5rem" }} role="status">
            <span className="visually-hidden">Cargando...</span>
          </div>
        </div>
      );
  }

  return (
    <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0, transition: { duration: 0.5 } }}
            exit={{ opacity: 0, y: -50, transition: { duration: 0.5 } }}
            className="page"
            >
    <div>
      <h2>Restablecer Contraseña</h2>
      <form onSubmit={handleSubmit}>
        <input
        className="form-control"
          type="password"
          placeholder="Nueva contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <br></br>
        <button className="btn btn-primary" type="submit">Restablecer</button>
      </form>
      {message && <p>{message}</p>}
    </div>
    </motion.div>
  );
};

export default ResetPassword;
