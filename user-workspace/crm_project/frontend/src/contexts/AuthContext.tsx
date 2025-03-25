import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { AuthState, LoginCredentials, User } from '../types/auth';
import axios from 'axios';

interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_URL = 'http://localhost:8000/api';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false,
  });

  useEffect(() => {
    if (authState.token) {
      fetchUser();
    }
  }, []);

  const fetchUser = async () => {
    try {
      const response = await axios.get(`${API_URL}/auth/user/`, {
        headers: { Authorization: `Bearer ${authState.token}` },
      });
      setAuthState(prev => ({
        ...prev,
        user: response.data,
        isAuthenticated: true,
      }));
    } catch (error) {
      logout();
    }
  };

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await axios.post(`${API_URL}/auth/login/`, credentials);
      const { access, user } = response.data;
      
      localStorage.setItem('token', access);
      
      setAuthState({
        user,
        token: access,
        isAuthenticated: true,
      });

      // Configure axios defaults
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
    } catch (error) {
      throw new Error('Login failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setAuthState({
      user: null,
      token: null,
      isAuthenticated: false,
    });
  };

  return (
    <AuthContext.Provider
      value={{
        ...authState,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}