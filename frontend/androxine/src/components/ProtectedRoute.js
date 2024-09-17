import { Navigate } from "react-router-dom";

import CircularProgress from '@mui/material/CircularProgress';

import { useAuth } from "../AuthProvider";


export const ProtectedRoute = ({ children }) => {
    const { isAuth, isGetAuthResponse } = useAuth();

    return (
        <>
            {
                !isGetAuthResponse
                    ? <CircularProgress />
                    : (
                        !isAuth
                            ? <Navigate to="/home" replace />
                            : children
                    )
            }
        </>
    );
};