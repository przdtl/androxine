import * as React from 'react';

import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import { alpha } from '@mui/material/styles';

import MainGrid from './MainGrid';
import SideMenu from './SideMenu';
import AppNavbar from './AppNavbar';
import ScrollToTopFab from './ScrollToTopFab';


export default function Dashboard({ children }) {
  return (
    <>
      <Box sx={{ display: 'flex' }}>
        <SideMenu />
        <AppNavbar />
        <Box
          component="main"
          sx={(theme) => ({
            flexGrow: 1,
            backgroundColor: alpha(theme.palette.background.default, 1),
            overflow: 'auto',
          })}
        >
          <Stack
            spacing={2}
            sx={{
              alignItems: 'center',
              mx: 3,
              pb: 10,
              mt: { xs: 8, md: 0 },
            }}
          >
            <MainGrid>
              {children}
              <ScrollToTopFab />
            </MainGrid>
          </Stack>
        </Box>
      </Box>
    </>
  );
}
