import React from "react";
import FileUpload from "./components/FileUpload";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <div className="App">
      <nav className="navbar navbar-dark bg-primary">
        <div className="container">
          <span className="navbar-brand mb-0 h1">JobMatch AI</span>
        </div>
      </nav>

      <FileUpload />
    </div>
  );
}

export default App;
