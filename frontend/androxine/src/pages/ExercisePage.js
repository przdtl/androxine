import Grid from '@mui/material/Grid2';
import SearchFilter from "../components/SearchFilter";
import TopBottomPagination from "../components/TopBottomPagination";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import { styled, alpha } from '@mui/material/styles';
import Toolbar from '@mui/material/Toolbar';

const exercise_categories = [
    { name: 'Legs' },
    { name: 'Biceps' },
    { name: 'Triceps' },
    { name: 'Shoulders' },
    { name: 'Chest' },
    { name: 'Back' },
    { name: 'Calves' },
    { name: 'Abs' },
    { name: 'Glute' },
    { name: 'Forearm' },
    { name: 'Cardio' },
]

const StyledToolbar = styled(Toolbar)(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    flexShrink: 0,
    borderRadius: `calc(${theme.shape.borderRadius}px + 8px)`,
    backdropFilter: 'blur(24px)',
    border: '1px solid',
    borderColor: theme.palette.divider,
    backgroundColor: alpha(theme.palette.background.default, 0.4),
    // boxShadow: theme.shadows[1],
    padding: '8px 12px',
}));

export default function ExercisePage() {
    return (
        <>
            <h1>
                Exercises
            </h1>
            <SearchFilter data={exercise_categories} />
            <TopBottomPagination>
                <Grid container rowSpacing={1}>
                    <StyledToolbar variant="dense" disableGutters>
                        <Box>
                            присед
                        </Box>
                        <Box>
                            ноги
                        </Box>
                    </StyledToolbar>
                    <StyledToolbar variant="dense" disableGutters>
                        <Box>
                            присед
                        </Box>
                        <Box>
                            ноги
                        </Box>
                    </StyledToolbar>
                    <StyledToolbar variant="dense" disableGutters>
                        <Box>
                            присед
                        </Box>
                        <Box>
                            ноги
                        </Box>
                    </StyledToolbar>
                    <StyledToolbar variant="dense" disableGutters>
                        <Box>
                            присед
                        </Box>
                        <Box>
                            ноги
                        </Box>
                    </StyledToolbar>
                    <StyledToolbar variant="dense" disableGutters>
                        <Box>
                            присед
                        </Box>
                        <Box>
                            ноги
                        </Box>
                    </StyledToolbar>
                    <StyledToolbar variant="dense" disableGutters>
                        <Box>
                            присед
                        </Box>
                        <Box>
                            ноги
                        </Box>
                    </StyledToolbar>
                </Grid>
            </TopBottomPagination>
        </>
    );
}