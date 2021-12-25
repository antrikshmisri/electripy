import React from "react";
import "./App.css";

import { eel } from "./eel.js";

const App = () => {
  eel.set_host("http://localhost:8888");
  return <></>;
};

export default App;
