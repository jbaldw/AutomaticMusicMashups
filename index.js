const express = require('express');
const path = require('path');
const fs = require('fs');
const multer = require('multer');

const PythonShell = require('python-shell').PythonShell;

const app = express();

// Create multer object to save mp3 files, filenames need to be temp1.mp3 and temp2.mp3
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, path.join(__dirname, 'public', 'audio'));
    },
    filename: function (req, file, cb) {
        cb(null, file.fieldname + '.mp3');
    }
});

const upload = multer({ storage: storage });

const port = 8080;

app.use(express.static(path.join(__dirname, 'public')));

// Route to index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Route to perform separation of mp3 file
app.post('/upload', upload.any('songs') , (req, res) => {
    // Run python script to separate the two mp3 files
    PythonShell.run(path.join(__dirname, 'public', 'python', 'separate.py'), null, (err) => {
        if(err) {
            throw err;
        }
    }).then(() => {
        // Run python script to vocode the two mp3 files
        PythonShell.run(path.join(__dirname, 'public', 'python', 'vocode_songs.py'), null, (err) => {
            if(err) {
                throw err;
            }
        }).then(() => {
            res.send('Success');
        });
    }).catch((err) => {
        console.log(err);
    });
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});