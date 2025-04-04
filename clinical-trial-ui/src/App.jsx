import React, { useState } from 'react';
import HomeComponent from './components/HomeComponent.jsx';
import ConsentFormComponent from './components/ConsentFormComponent.jsx';
import DownloadPDFComponent from './components/DownloadPDFComponent.jsx';
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import './App.css';
import './transitions.css';

function App() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [formOption, setFormOption] = useState('');
  const [textAreaData, setTextAreaData] = useState({});
  const [showConsentForm, setShowConsentForm] = useState(false);
  const [showDownloadPDF, setShowDownloadPDF] = useState(false);

  const handleFilesSelected = (files) => {
    setSelectedFiles(files);
  };

  const handleFormOptionSelected = (option) => {
    if (option === 'Consent Form') {
      setFormOption(option);
      setShowConsentForm(true);
    } else {
      alert('This option is not implemented yet.');
    }
  };

  const handleTextAreaDataUpdate = (data) => {
    setTextAreaData(data);
  };

  const handleRestart = () => {
    // Reset all states to initial values
    setSelectedFiles([]);
    setFormOption('');
    setTextAreaData({});
    setShowConsentForm(false);
  };

  return (
    <div className="App">
       <TransitionGroup>
      {!showConsentForm && !showDownloadPDF ? (
        <HomeComponent
          onFilesSelected={handleFilesSelected}
          onFormOptionSelected={handleFormOptionSelected}
        />
      ) : showConsentForm && !showDownloadPDF ? (
        <>
          <ConsentFormComponent
            selectedFiles={selectedFiles}
            textAreaData={textAreaData}
            onTextAreaDataUpdate={handleTextAreaDataUpdate}
          />

        </>
      )
      : showDownloadPDF ? (
        <>
        <DownloadPDFComponent textAreaData={textAreaData} />
        <button onClick={handleRestart}>Restart</button>
        </>
      ) : null
      }
      </TransitionGroup>
    </div>
  );
}

export default App;