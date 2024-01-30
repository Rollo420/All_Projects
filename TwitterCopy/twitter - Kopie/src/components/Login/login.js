import React, { useState } from 'react';
import axios from 'axios';
import './css/login.css';
import { useNavigate , useLocation} from 'react-router-dom';

export default function Login() {
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const logoutInfoVar = useLocation();

    const loginUser = async () => {
        try {
            const response = await axios.post('http://localhost:5000/login', { name, password });
            navigate('/design', {state: { username : name, login: true} }); 
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="main">
            <div className="wrapperr">
                <div className="signin">
                    <div className="content">
                        <p>{logoutInfoVar?.state?.info?.logoutInfo}</p>
                        <h2>Login</h2>
                        <div className="form">
                            <div className="inputBox">
                                <input type="text" placeholder="Username/Email" required value={name} onChange={(e) => setName(e.target.value)}/>
                            </div>
                            <div className="inputBox">
                                <input type="password" placeholder="Password" required value={password} onChange={(e) => setPassword(e.target.value)}/>
                            </div>
                            <div class="links"> <a href="#">Forgot Password?</a> <a href="/register">Signup</a> </div>
                            <div className="inputBox">
                                <input type="submit" onClick={loginUser} value="Sign In"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
