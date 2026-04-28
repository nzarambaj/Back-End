const express = require('express');
const router = express.Router();
const { authMiddleware } = require('../middleware/auth');
const {
  login,
  register,
  getMe,
  logout
} = require('../controllers/auth.controller');

// Public routes
router.post('/login', login);
router.post('/register', register);

// Protected routes
router.get('/me', authMiddleware, getMe);
router.post('/logout', authMiddleware, logout);

module.exports = router;
