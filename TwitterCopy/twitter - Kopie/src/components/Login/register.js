import React, { useState } from 'react';
import axios from 'axios';
import {useNavigate } from 'react-router-dom';
//import Design from './../Main/Design';

const bcrypt = require('bcryptjs');
const saltRounds = 10; // Anzahl der Salt-Runden


async function passHash(password) {
    // Erzeuge ein Salt und hashe das Passwort
    const hashedPassword = await bcrypt.hash(password, saltRounds);
    
    // Hier könntest du das gehashte Passwort in der Datenbank speichern
    return hashedPassword;
}


export default function Register() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] =useState('');
    const navigate = useNavigate();
    const [registerError, setRegisterError] = useState(null)

    const addUser = async () => {
        
    
        try {
            const hashedPassword = await passHash(password);
            const response = await axios.post('http://localhost:5000/register', { name, email, password: hashedPassword });
            
            setRegisterError(response.data); // Korrigiere den Tippfehler
            
         } catch (err) {
            console.error(err);
         }
    };

    

    return (
        <div className="main">
            <div className="wrapperr">
                <div className="signin">
                    <div className="content">
                        <h2>Sign In</h2>
                        <p>{registerError}</p>
                        <div className="form">
                            <div className="inputBox">
                                <input type="text" placeholder="Username" required value={name} onChange={e => setName(e.target.value)}/>
                            </div>
                            <div className="inputBox">
                                <input type="text" placeholder="Email" required value={email} onChange={e => setEmail(e.target.value)}/>
                            </div>
                            <div className="inputBox">
                                <input type="password" placeholder="Password" required value={password} onChange={e => setPassword(e.target.value)}/>
                            </div>
                            <div class="links"> <a href="#"></a> <a href="/login">Already got an account?</a> </div>
                            <div className="inputBox">
                                <input type="submit" onClick={addUser} value="Create your account"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}