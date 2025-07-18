import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { MainPage } from './screens/MainPage';
import { PracticePage } from './screens/PracticePage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/practice" element={<PracticePage />} />
        <Route path="/practice/:songName" element={<PracticePage />} />
      </Routes>
    </Router>
  );
}

export default App;