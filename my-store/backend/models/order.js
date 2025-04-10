const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema({

    user:[ {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'user'
    }],

    products: [{
        product: { type: mongoose.Schema.Types.ObjectId, ref: 'Product' },
        quantity: Number
    }],

    status: {
    type: String,
    enum: ['בהמתנה', 'מאושר', 'נדחה'],
    default: 'בהמתנה'
    },
 
  
});

module.exports = mongoose.model('Order', orderSchema);
