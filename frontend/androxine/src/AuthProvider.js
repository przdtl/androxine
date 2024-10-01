import axios from 'axios'

import React, { createContext, useContext, useEffect, useState } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuth, setIsAuth] = useState(false);
    const [isGetAuthResponse, setIsGetAuthResponse] = useState(false);
    const [user, setUser] = useState(null);
    const [csrfToken, setCsrfToken] = useState('');

    const login = (user_obj) => {
        setIsAuth(true);
        setUser(user_obj);
    };

    const logout = () => {
        setIsAuth(false);
        setUser(null);
    };

    useEffect(() => {
        getSession();
    }, [isAuth]);

    const getCSRF = () => {
        axios.get(process.env.REACT_APP_BACKEND_API_URL + 'auth/csrf/', { withCredentials: true })
            .then((res) => {
                const token = res.headers.get('X-CSRFToken');
                setCsrfToken(token);
            })
            .catch(err => { console.error(err) })
    };

    const getSession = () => {
        axios.get(process.env.REACT_APP_BACKEND_API_URL + 'auth/me/', { withCredentials: true })
            .then(response => {
                login(response.data);
                getCSRF();
            })
            .catch(error => {
                console.log(error);
            })
            .finally(() => {
                setIsGetAuthResponse(true);
            });
    };


    return (
        <AuthContext.Provider value={{ isAuth, user, login, logout, isGetAuthResponse, csrfToken, getCSRF }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};
