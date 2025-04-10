const userRoute = require('./routes/user');
const productRoute = require('./routes/product'); 

const express = require('express');
const cors = require('cors');
const app = express();
app.use(express.json());
app.use(cors());
   
app.use('/user', userRoute);
app.use('/product', productRoute);

require('dotenv').config()
const mongoose = require('mongoose')

mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB error:', err));

app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).send('An error in app, please try later.')
})

const PORT = 5000
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
