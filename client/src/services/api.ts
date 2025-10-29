import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  async sendMessage(message: string) {
    const response = await apiClient.post('/chat', { message });
    return response.data;
  },
};

export default api;
