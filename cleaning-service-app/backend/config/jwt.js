const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';
const JWT_EXPIRY = '7d';

module.exports = {
  JWT_SECRET,
  JWT_EXPIRY
};
