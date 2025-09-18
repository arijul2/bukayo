import React from "react";
import FileUpload from "./components/FileUpload";
import JobDescriptionUpload from "./components/JobDescriptionUpload";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <div className="App">
      <nav className="navbar navbar-dark bg-primary">
        <div className="container">
          <span className="navbar-brand mb-0 h1">JobMatch AI</span>
        </div>
      </nav>

      <div className="container-fluid">
        <div className="row">
          <div className="col-md-6">
            <FileUpload />
          </div>
          <div className="col-md-6">
            <JobDescriptionUpload />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
