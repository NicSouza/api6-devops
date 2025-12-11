// apps/web/src/service/config.ts
export const getApiBaseUrl = () => import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';
export const getAuthBaseUrl = () => import.meta.env.VITE_AUTH_BASE_URL || 'http://127.0.0.1:3000';
export const getPredictionBaseUrl = () => import.meta.env.VITE_API_PREDICTION_URL || 'http://127.0.0.1:9000';
