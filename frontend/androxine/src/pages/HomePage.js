import Link from '@mui/material/Link';
import HomeIcon from '@mui/icons-material/Home';
import WhatshotIcon from '@mui/icons-material/Whatshot';
import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import Breadcrumbs, { breadcrumbsClasses } from '@mui/material/Breadcrumbs';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateNextRoundedIcon from '@mui/icons-material/NavigateNextRounded';

const StyledBreadcrumbs = styled(Breadcrumbs)(({ theme }) => ({
    margin: theme.spacing(1, 0),
    [`& .${breadcrumbsClasses.separator}`]: {
        color: theme.palette.action.disabled,
        margin: 1,
    },
    [`& .${breadcrumbsClasses.ol}`]: {
        alignItems: 'center',
    },
}));

export default function HomePage() {
    return (
        <>
            <StyledBreadcrumbs
                aria-label="breadcrumb"
                separator={<NavigateNextRoundedIcon fontSize="small" />}
            >
                <Typography />
                <Typography variant="body1" sx={{ color: 'text.primary', fontWeight: 600 }}>
                    Home
                </Typography>
            </StyledBreadcrumbs>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>
            <h1>
                HomePage
            </h1>

        </>
    );
}
