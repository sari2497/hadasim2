const express = require("express");
const router = express.Router();
const productService = require("../services/product"); // שירות המוצרים

// הוספת מוצרים למשתמש
router.post("/addProducts", async (req, res) => {
  try {
    const { email, products } = req.body;

    if (!email || !products || products.length === 0) {
      return res.status(400).json({ error: 'חסרים שדות' });
    }

    console.log("Adding products for email:", email);
    const createdProducts = await productService.addProducts(email, products);

    res.status(201).json({ message: 'המוצרים נוספו בהצלחה', products: createdProducts });
  } catch (err) {
    console.error("Error adding products:", err);
    res.status(500).json({ error: 'שגיאה בהוספת מוצרים' });
  }
});

module.exports = router;
