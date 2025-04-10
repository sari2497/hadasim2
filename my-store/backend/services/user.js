const User = require("../models/User");


class UserService {
    async registerUser(fullName, phone, email, companyName, products) {
    // יצירת משתמש בסיס
            const newUser = new User({ fullName, phone, email, role: 'supplier', companyName, products});
            await newUser.save();
    
        return { message: "משתמש נוצר בהצלחה", user: newUser };
    } 

    
}
  
let userService = new UserService();
module.exports = userService;



