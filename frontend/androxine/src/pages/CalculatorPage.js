import Box from '@mui/material/Box';

import Typography from '@mui/material/Typography';
import { PageCard, PageCardContainer } from '../components/PageCard';


export default function CalculatorPage() {
    return (
        <>
            <PageCardContainer direction="column" justifyContent="space-between">
                <PageCard variant="outlined">
                    <Typography
                        component="h1"
                        variant="h5"
                        sx={{ width: '100%' }}
                    >
                        Calculator
                    </Typography>
                    <Box
                        component="form"
                        // onSubmit={handleSubmit}
                        noValidate
                        sx={{
                            display: 'flex',
                            flexDirection: 'column',
                            width: '100%',
                            gap: 2,
                        }}
                    >
                        <Typography variant='bady1'>
                            row
                        </Typography>
                    </Box>
                </PageCard>
            </PageCardContainer>
        </>
    );
}