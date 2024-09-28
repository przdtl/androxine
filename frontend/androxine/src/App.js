import React from 'react';
import { SnackbarProvider } from 'notistack'

import { BrowserRouter, Routes, Route } from 'react-router-dom';

import * as locales from '@mui/material/locale';
import { createTheme, ThemeProvider, useColorScheme, responsiveFontSizes } from '@mui/material/styles';

import getTheme from './theme/getTheme';
import { AuthProvider } from './AuthProvider';
import { useLocale } from './LocaleProvider';

import './App.css';
import '@fontsource/inter/600.css';

import HomePage from './pages/HomePage';
import WeightPage from './pages/WeightPage';
import SignInPage from './pages/SignInPage';
import SignUpPage from './pages/SignUpPage';
import WorkoutPage from './pages/WorkoutPage';
import ProfilePage from './pages/ProfilePage';
import ExercisePage from './pages/ExercisePage';
import SettingsPage from './pages/SettingsPage';
import TemplatePage from './pages/TemplatePage';
import NotFoundPage from './pages/NotFoundPage';
import CalculatorPage from './pages/CalculatorPage';
import { AuthTokenVerifyPage } from './pages/AuthTokenVerifyPage';

import Dashboard from './components/Dashboard';
import { ProtectedRoute } from './components/ProtectedRoute';
import SnackbarCloseButton from './components/SnackbarCloseButton';


export const App = () => {
  const { mode } = useColorScheme();
  const { locale } = useLocale();

  const theme = React.useMemo(
    () => createTheme(getTheme(mode), locales[locale]),
    [locale],
  );

  return (
    <>
      <ThemeProvider theme={theme} >
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
                  <Dashboard>
                    <ExercisePage />
                  </Dashboard>
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
                <Route path="/settings" element={
                  <Dashboard>
                    <SettingsPage />
                  </Dashboard>
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
