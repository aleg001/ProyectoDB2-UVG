import logo from "./logo.svg";
import "./App.css";
import React, { useEffect, useState } from "react";
import axios from "axios";
//import Login from "./login.js";

//import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  const [getMessage, setGetMessage] = useState({});

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/")
      .then((response) => {
        console.log("SUCCESS", response);
        setGetMessage(response);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Proyecto 2 - BD</p>
        <div>
          {getMessage.status === 200 ? (
            <h3>{getMessage.data.message}</h3>
          ) : (
            <h3>Login</h3>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
