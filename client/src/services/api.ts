import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  async sendMessage(message: string, sessionId?: string) {
    const response = await apiClient.post('/chat', { message, session_id: sessionId });
    return response.data;
  },
};

export default api;
