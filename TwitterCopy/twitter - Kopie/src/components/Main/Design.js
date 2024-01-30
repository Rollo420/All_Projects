import React, { useEffect, useState } from 'react';
import './css/Design.css';
import logo from './logo.svg';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import io from 'socket.io-client';

import Chat from './../Chat/Chat'

export default function Design() {
  const navigate = useNavigate();
  const { state } = useLocation();

  const socket = io('http://localhost:5000');
  let [userStats, setUserStats] = useState('');

  useEffect(() => {
    const checkSession = async () => {
      try {
        // Prüfen, ob der Benutzer angemeldet ist
        if (state && state.login === true) {
          try {
            const response = await axios.post('http://localhost:5000/loadeUser', {
              username: state.username,
            });

            // Setze die Benutzerstatistik im State
            setUserStats(response.data);
          } catch (err) {
            console.error(err);
          }
        } else {
          // Wenn der Benutzer nicht angemeldet ist, zur Login-Seite navigieren
          navigate('/login', {
            state: { info: { logoutInfo: 'Sie müssen sich einloggen' } },
          });
        }
      } catch (error) {
        console.error(error);
      }
    };

    checkSession();
  }, [state, navigate]);

 
  const handleLogout = () => {
    navigate('/login', { state: null });
  };

  return (
    <div className="container">
      <div className="icon">
        <img src={logo} alt="Logo" />
      </div>
      <div class="user-banner">
        <div>
          <p className="welcome">
            Welcome, {state?.username ? state?.username : 'Gust'}
          </p>
          <p className="level">Level {Math.floor(userStats?.playerLevel)}</p>
        </div>
        <button onClick={handleLogout} className="logout-bttn"></button>        
      </div>
      <div class="top-banner"></div>
      <div class="sidebar">
        <div className="nav-item"></div>
        <div className="nav-item"></div>
        <div className="nav-item"></div>
        <div className="nav-item"></div>
        <div className="nav-item"></div>
        <div className="nav-item"></div>
        <div className="nav-item"></div>
        <div className="nav-item"></div>
      </div>
      <div class="chatbox">
        <div class="chats">
          <h3>Chats</h3>
          <div class="chat">
            <p className="chat-name">#general</p>
            <p className="chat-name">#politics</p>
            <p className="chat-name">#crypto</p>
            <p className="chat-name">#gaming</p>
            <p className="chat-name">###</p>
            <p className="chat-name">###</p>
            <p className="chat-name">###</p>
            <p className="chat-name">###</p>
          </div>
        </div>
        <div class="messageboard">
          <div class="header">
            <div class="chat-icon"></div>
            <h3>#general</h3>
            <p>### online</p>
            <button className="follow-chat-bttn"></button>
          </div>
          <div class="messages">
            <p>Hier ist der Chat</p>
            
          </div>
        </div>
      </div>
      <div class="x"></div>
    </div>
  );
}
