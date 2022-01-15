import React from "react";
import Button from "./components/Button";
import Paragraph from "./components/Paragraph";
import Image from "./components/Image";

// import { eel } from "./eel.js";

const App = () => {
  // eel.set_host("http://localhost:8888");
  return (
    <Button
      id="1234"
      className="btn"
      onClick={() => {
        console.log("Clicked");
      }}
      style={{ backgroundColor: "#f5f5dc", width: "100px", height: "50px" }}
    >
      <Paragraph id="2312" className="btn-text" text="Electripy" />
      <Image
        alt="python icon"
        src="https://img.icons8.com/ios-glyphs/344/python.png"
        size={[200, 200]}
        id="2131"
        className="btn-logo"
      />
    </Button>
  );
};

export default App;
