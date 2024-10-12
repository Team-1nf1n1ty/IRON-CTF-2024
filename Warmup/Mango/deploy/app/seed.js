const mongoose = require('mongoose');
const Admin = require('./models/Admin');

async function createAdmin() {
    const admin = new Admin({ username: 'admin', password: 'iL0v3M@Ng0s!' });
    await admin.save();
    console.log('Admin created');
    mongoose.connection.close();
}

mongoose.connect('mongodb://mongo-mango:27017/mango', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(createAdmin);
