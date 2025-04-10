const express = require("express");
const router = express.Router();
const userService = require("../services/user");
const productService = require("../services/product"); // הוספנו את שירות המוצרים

// רישום משתמש חדש
router.post("/register", async (req, res) => {
  console.log("Starting user registration");
  try {
    const { fullName, phone, email, companyName, products } = req.body;
    console.log("Received data:", fullName, phone, email, companyName, products);
    
    if (!fullName || !phone || !email) {
      return res.status(400).json({ error: "חסרים שדות בהרשמה" });
    }

    const result = await userService.registerUser(
      fullName,
      phone,
      email,
      companyName,
      products
    );

    // לאחר יצירת המשתמש, נוודא שהמוצרים שנשלחו מתווספים למשתמש
    if (products && products.length > 0) {
      console.log("Redirecting to add products route");
      await productService.addProducts(email, products);
    }

    res.json(result);
  } catch (err) {
    console.error("Error during registration:", err);
    res.status(500).json({ error: "שגיאה בשרת" });
  }
});

module.exports = router;
