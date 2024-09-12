import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import getTheme from './theme/getTheme';
import Dashboard from './components/Dashboard';
import { AuthProvider } from './UserProvider';

import './App.css';
import '@fontsource/inter/600.css';

import NotFoundPage from './pages/NotFoundPage';
import HomePage from './pages/HomePage';
import SignInPage from './pages/SignInPage';
import SignUpPage from './pages/SignUpPage';
import ExercisePage from './pages/ExercisePage';
import TemplatePage from './pages/TemplatePage';
import WorkoutPage from './pages/WorkoutPage';
import WeightPage from './pages/WeightPage';
import ProfilePage from './pages/ProfilePage';
import CalculatorPage from './pages/CalculatorPage';

export const App = () => {
  const Theme = createTheme(getTheme('light'));

  return (
    <>
      <ThemeProvider theme={Theme}>
        <AuthProvider>
          <BrowserRouter>
            <Routes>
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
                <Dashboard>
                  <ProfilePage />
                </Dashboard>
              } />
              <Route path="/template" element={
                <Dashboard>
                  <TemplatePage />
                </Dashboard>
              } />
              <Route path="/workout" element={
                <Dashboard>
                  <WorkoutPage />
                </Dashboard>
              } />
              <Route path="/weight" element={
                <Dashboard>
                  <WeightPage />
                </Dashboard>
              } />
              <Route path="/sign-in" element={<SignInPage />} />
              <Route path="/sign-up" element={<SignUpPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </ThemeProvider>
    </>
  );
}
