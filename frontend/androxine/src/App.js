import React from 'react';
import { SnackbarProvider } from 'notistack'

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { createTheme, ThemeProvider, responsiveFontSizes } from '@mui/material/styles';

import getTheme from './theme/getTheme';
import { AuthProvider } from './AuthProvider';

import './App.css';
import '@fontsource/inter/600.css';

import HomePage from './pages/HomePage';
import WeightPage from './pages/WeightPage';
import SignInPage from './pages/SignInPage';
import SignUpPage from './pages/SignUpPage';
import WorkoutPage from './pages/WorkoutPage';
import ProfilePage from './pages/ProfilePage';
import Dashboard from './components/Dashboard';
import ExercisePage from './pages/ExercisePage';
import TemplatePage from './pages/TemplatePage';
import NotFoundPage from './pages/NotFoundPage';
import CalculatorPage from './pages/CalculatorPage';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthTokenVerifyPage } from './pages/AuthTokenVerifyPage';

import SnackbarCloseButton from './SnackbarCloseButton';


export const App = () => {
  let Theme = createTheme(getTheme('light'));
  Theme = responsiveFontSizes(Theme, { breakpoints: ['xs', 'sm', 'md', 'lg', 'xl'], factor: 4 });

  return (
    <>
      <ThemeProvider theme={Theme} >
        <AuthProvider>
          <SnackbarProvider action={snackbarKey => <SnackbarCloseButton snackbarKey={snackbarKey} />}>
            <BrowserRouter>
              <Routes>
                <Route path="/profile/activate" element={<AuthTokenVerifyPage />} />
                <Route path="/sign-in" element={<SignInPage />} />
                <Route path="/sign-up" element={<SignUpPage />} />
                <Route path="/home" element={
                  <Dashboard>
                    <HomePage />
                  </Dashboard>
                } />
                <Route path="/exercise" element={
                  <ProtectedRoute>
                    <Dashboard>
                      <ExercisePage />
                    </Dashboard>
                  </ProtectedRoute>
                } />
                <Route path="/calculator" element={
                  <Dashboard>
                    <CalculatorPage />
                  </Dashboard>
                } />
                <Route path="/profile" element={
                  <ProtectedRoute>
                    <Dashboard>
                      <ProfilePage />
                    </Dashboard>
                  </ProtectedRoute>
                } />
                <Route path="/template" element={
                  <ProtectedRoute>
                    <Dashboard>
                      <TemplatePage />
                    </Dashboard>
                  </ProtectedRoute>
                } />
                <Route path="/workout" element={
                  <ProtectedRoute>
                    <Dashboard>
                      <WorkoutPage />
                    </Dashboard>
                  </ProtectedRoute>
                } />
                <Route path="/weight" element={
                  <ProtectedRoute>
                    <Dashboard>
                      <WeightPage />
                    </Dashboard>
                  </ProtectedRoute>
                } />
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </BrowserRouter>
          </SnackbarProvider>
        </AuthProvider>
      </ThemeProvider >
    </>
  );
}
