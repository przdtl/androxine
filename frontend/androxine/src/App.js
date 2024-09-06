import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { NotFoundPage } from './pages/NotFoundPage';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import SignInPage from './pages/SignInPage';
import getTheme from './theme/getTheme';
import SignUpPage from './pages/SignUpPage';
import Dashboard from './components/Dashboard';
import { AuthProvider } from './UserProvider';

import './App.css';
import '@fontsource/inter/600.css';




export const App = () => {
  const Theme = createTheme(getTheme('light'));

  return (
    <>
      <ThemeProvider theme={Theme}>
        <AuthProvider>
          <BrowserRouter>
            <Routes>
              <Route element={<Dashboard />}>
                <Route path="/" element={<HomePage />} />
              </Route>
              <Route path="/sign-in" element={<SignInPage />} />
              <Route path="/sign-up" element={<SignUpPage />} />
              <Route path="/exercise" />
              <Route path="/calculator" />
              <Route path="/profile" />
              <Route path="/template" />
              <Route path="/workout" />
              <Route path="/weight" />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </ThemeProvider>
    </>
  );
}
