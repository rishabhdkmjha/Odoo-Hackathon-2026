import { createContext, useEffect, useState } from 'react';
import * as authService from '../services/authService';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const cachedUser = localStorage.getItem('assetflow_user');
    const token = localStorage.getItem('assetflow_token');
    if (cachedUser && token) {
      setUser(JSON.parse(cachedUser));
    }
    setIsLoading(false);
  }, []);

  const login = async (credentials) => {
    const { token, user: loggedInUser } = await authService.login(credentials);
    localStorage.setItem('assetflow_token', token);
    localStorage.setItem('assetflow_user', JSON.stringify(loggedInUser));
    setUser(loggedInUser);
    return loggedInUser;
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, isAuthenticated: !!user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
