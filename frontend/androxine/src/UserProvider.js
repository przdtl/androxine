import React, { createContext, useContext, useState } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuth, setIsAuth] = useState(false);
    const [user, setUser] = useState(null);

    const login = () => {
        setIsAuth(true);
    };

    const logout = () => {
        setIsAuth(false);
    };

    return (
        <AuthContext.Provider value={{ isAuth, user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};