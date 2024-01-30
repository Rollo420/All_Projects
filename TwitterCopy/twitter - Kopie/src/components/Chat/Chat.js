import React, { useEffect, useState } from "react";
import axios from 'axios';
import queryString from "query-string";
import io  from 'socket.io-client';

let socket
const Chat  = () => {
    
    const username = 'woodly'
    const [ChatID, setChatID] = useState('');  
    const ENDPOINT = 'http://localhost:5000'

    const getChatID = async () => {
            
        try {
            const response = await axios.post('http://localhost:5000/loadePrivateUserChats', {username: username});
            
            setChatID(response.data.ChatID); 
            
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        getChatID();
    
        socket = io(ENDPOINT);
        socket.emit('join', { name: username, room: ChatID });
    
        // Überprüfen, ob der Socket verbunden ist
        alert('Socket connected:', socket.connected);
    
        socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });
    
        return () => {
            if (socket) {
                socket.disconnect();
            }
        };
    }, [ENDPOINT, ChatID, username]);
    
    


    return (
        <h1>Hello Chat</h1>
    )
}

export default Chat;