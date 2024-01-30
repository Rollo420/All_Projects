import React from 'react';
import './css/App.css';
import Design from './components/Main/Design';
import Login from './components/Login/login';
import Register from './components/Login/register';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <div className="wrapper">
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/design" element={<Design />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;


//npm init -y
//npm install express mysql
//npm install axios
//npm install crypto-browserify