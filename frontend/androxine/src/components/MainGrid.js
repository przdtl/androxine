import * as React from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';


export default function MainGrid({ children }) {
  return (
    <Box sx={{ width: '100%', maxWidth: { sm: '100%', md: '1700px' } }}>
      <Container
        maxWidth="xl"
        component="main"
        sx={{ display: 'flex', flexDirection: 'column', my: 4, gap: 4 }}
      >
        {children}
      </Container>
    </Box>
  );
}
