

import axios from 'axios';

const API_URL = 'http://localhost:56396';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the token in all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Authentication services
export const authService = {
  login: async (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    const response = await api.post('/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  },
  
  register: async (userData) => {
    return api.post('/users/', userData);
  },
  
  logout: () => {
    localStorage.removeItem('token');
  },
  
  getCurrentUser: async () => {
    return api.get('/users/me/');
  },
};

// User profile services
export const profileService = {
  getMyProfile: async () => {
    return api.get('/profiles/me/');
  },
  
  createProfile: async (profileData) => {
    return api.post('/profiles/', profileData);
  },
  
  updateProfile: async (profileData) => {
    return api.put('/profiles/me/', profileData);
  },
  
  getUserProfile: async (userId) => {
    return api.get(`/profiles/${userId}`);
  },
};

// Photo services
export const photoService = {
  uploadPhoto: async (file, isPrimary = false, visibility = 'all') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('is_primary', isPrimary);
    formData.append('visibility', visibility);
    
    return api.post('/photos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  getMyPhotos: async () => {
    return api.get('/photos/me/');
  },
  
  getUserPhotos: async (userId) => {
    return api.get(`/photos/${userId}`);
  },
  
  deletePhoto: async (photoId) => {
    return api.delete(`/photos/${photoId}`);
  },
};

// Match preference services
export const preferenceService = {
  getMyPreferences: async () => {
    return api.get('/preferences/me/');
  },
  
  createPreferences: async (preferenceData) => {
    return api.post('/preferences/', preferenceData);
  },
  
  updatePreferences: async (preferenceData) => {
    return api.put('/preferences/me/', preferenceData);
  },
};

// Family detail services
export const familyService = {
  getMyFamilyDetails: async () => {
    return api.get('/family/me/');
  },
  
  createFamilyDetails: async (familyData) => {
    return api.post('/family/', familyData);
  },
  
  updateFamilyDetails: async (familyData) => {
    return api.put('/family/me/', familyData);
  },
  
  getUserFamilyDetails: async (userId) => {
    return api.get(`/family/${userId}`);
  },
};

// Connection services
export const connectionService = {
  sendInterest: async (receiverId) => {
    return api.post('/connections/', { receiver_id: receiverId, status: 'pending' });
  },
  
  getMyConnections: async (status = null) => {
    const params = status ? { status } : {};
    return api.get('/connections/', { params });
  },
  
  updateConnectionStatus: async (connectionId, status) => {
    return api.put(`/connections/${connectionId}`, { status });
  },
};

// Message services
export const messageService = {
  sendMessage: async (receiverId, messageText) => {
    return api.post('/messages/', { receiver_id: receiverId, message_text: messageText });
  },
  
  getConversation: async (userId, skip = 0, limit = 100) => {
    return api.get(`/messages/${userId}`, { params: { skip, limit } });
  },
  
  markMessageAsRead: async (messageId) => {
    return api.put(`/messages/${messageId}/read`);
  },
};

// Membership services
export const membershipService = {
  getMyMembership: async () => {
    return api.get('/memberships/me/');
  },
  
  createMembership: async (membershipData) => {
    return api.post('/memberships/', membershipData);
  },
  
  updateMembership: async (membershipData) => {
    return api.put('/memberships/me/', membershipData);
  },
};

// Success story services
export const successStoryService = {
  getSuccessStories: async (approvedOnly = true, featuredOnly = false, skip = 0, limit = 100) => {
    return api.get('/success-stories/', {
      params: { approved_only: approvedOnly, featured_only: featuredOnly, skip, limit },
    });
  },
  
  getSuccessStory: async (storyId) => {
    return api.get(`/success-stories/${storyId}`);
  },
  
  createSuccessStory: async (storyData) => {
    return api.post('/success-stories/', storyData);
  },
  
  uploadStoryPhoto: async (storyId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return api.post(`/success-stories/${storyId}/photos`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  getStoryPhotos: async (storyId) => {
    return api.get(`/success-stories/${storyId}/photos`);
  },
};

// Match finding services
export const matchService = {
  findMatches: async (skip = 0, limit = 20) => {
    return api.get('/matches/', { params: { skip, limit } });
  },
};

export default api;

