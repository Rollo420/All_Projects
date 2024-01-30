const express = require('express');
const mysql = require('mysql');
const cors = require('cors');
const bodyParser = require('body-parser');
const bcrypt = require('bcryptjs');
const credentials = require('../dbConfig.js');
const http = require('http');
const fs = require('fs');
const path = require('path');
const socketIo = require('socket.io');

const React = require('react');

const router = require('./router');


const app = express();
app.use(cors());
app.use(bodyParser.json());

const server = http.createServer(app);
const io = socketIo(server);


const db = mysql.createConnection({
    ...credentials
});

db.connect((err) => {
    if (err) throw err;
    console.log('Connected to the database.');
});

io.on('connection', (socket) => {
    console.log('We have a new connection!!!');

    socket.on('join', ({ username, ChatID }) => {
        console.log('Das ist out: ' + username, ChatID);
    });

    socket.on('disconnect', () => {
        console.log('User had left!!!');
    });
});

app.post('/register', (req, res) => {

    const { name, email, password } = req.body;

    const querySelect = 'SELECT email, username FROM users WHERE email = ? OR username = ?';
    const queryInsert = 'INSERT INTO users (username, email, password, playerLevel ,createDate) VALUES (?, ?, ?, ?, ?)';
    

    db.query(querySelect, [email, name], (err, resultSelect) => {
        if (err) {
            console.error(err);
            res.status(500).send('An error occurred.');
            return;
        }

        // Überprüfe, ob ein Ergebnis zurückgegeben wurde
        if (resultSelect.length > 0) {
            // E-Mail ist bereits in der Datenbank vorhanden
            console.log('Die E-Mail-Adresse oder der Username ist bereits registriert.');
            // Hier könntest du entsprechend reagieren, z.B. eine Fehlermeldung senden
            res.status(200).send('Die E-Mail-Adresse oder\nder Username ist bereits registriert.');
        } else {
            // E-Mail ist noch nicht in der Datenbank vorhanden
            console.log('Die E-Mail-Adresse ist noch nicht registriert.');
            //Erstellt das Aktuelle Datum und Uhrzeit
            let date = new Date();
            // Füge den neuen Benutzer zur Datenbank hinzu (Beispielcode)
            db.query(queryInsert, [name, email, password, 1.100 ,date], (err, resultInsert) => {
                if (err) {
                    console.error(err);
                    res.status(500).send('An error occurred.');
                    return;
                }
                // Hier könntest du entsprechend reagieren, z.B. eine Erfolgsmeldung senden
                res.status(200).send('Registrierung erfolgreich.');
            });
        }
    });

});


app.post('/login', (req, res) => {
    const { name, password } = req.body;
    const querySelect = 'SELECT username, email, password FROM users WHERE username = ? OR email = ?';

    db.query(querySelect, [name, name], async (err, result) => {
        if (err) {
            console.error(err);
            res.status(500).send('An error occurred.');
            return;
        }

        // Überprüfen, ob Ergebnisse vorhanden sind
        if (result.length > 0) {
            try {
                const passwordMatch = await bcrypt.compare(password, result[0].password);

                if ((name === result[0].username || name === result[0].email) && passwordMatch) {
                    res.status(200).send('Login successfully');
                } else {
                    res.status(401).send('Login fehlgeschlagen.');
                }
            } catch (error) {
                console.error(error);
                res.status(500).send('An error occurred.');
            }
        }
        else {res.status(401).send('Login fehlgeschlagen.');}


    });
});


app.post('/loadeUser', (req, res) => {
    const { username } = req.body;
    
    const querySelect = 'SELECT username, playerLevel FROM users WHERE username = ? OR email = ?';
    
    db.query(querySelect, [username, username], async (err, result) => {
        if (err) {
            console.error(err);
            res.status(500).send('An error occurred.');
            return;
        }

        res.status(200).send(result[0]);
        
    });
    
});

app.post('/loadePrivateUserChats', (req, res) => {
    const { username } = req.body;
    const querySelectChat = 'SELECT privateuserchat.username, privateuserchat.ChatID FROM `privateuserchat` INNER JOIN users on privateuserchat.username = users.username;';
    db.query(querySelectChat, [username], async (err, result) => {
        if (err) {
            console.error(err);
            res.status(500).send('An error occurred.');
            return;
        }
        console.log(result);
        res.status(200).send(result[0]);
    });
});


app.listen(5000, () => console.log('Server is running on port 5000.'));