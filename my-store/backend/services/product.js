
const Product = require('../models/product');
const User = require('../models/User');

class ProductService {
  async addProducts(userEmail, products) {
    const user = await User.findOne({ email: userEmail });

    if (!user) {
      throw new Error('משתמש לא נמצא');
    }

    const createdProducts = await Promise.all(
      products.map(product => {
        const newProduct = new Product({
          name: product.name,
          price: product.price,
          minQuantity: product.minQuantity,
          user: user._id,  // נוודא שהמוצר מקושר למשתמש
        });
        return newProduct.save();
      })
    );

    // עדכון המוצרים במודל המשתמש
    user.products.push(...createdProducts.map(p => p._id));
    await user.save();

    return createdProducts;
  }
}

module.exports = new ProductService();
