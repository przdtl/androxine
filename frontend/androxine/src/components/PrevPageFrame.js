import * as React from 'react';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import { styled } from '@mui/material/styles';
import IconButton from '@mui/material/IconButton';
import ArrowBackRoundedIcon from '@mui/icons-material/ArrowBackRounded';


const StyledAppBar = styled(AppBar)(({ theme }) => ({
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    flexShrink: 0,
    borderBottom: '1px solid',
    borderColor: theme.palette.divider,
    backgroundColor: theme.palette.background.paper,
    boxShadow: 'none',
    backgroundImage: 'none',
    zIndex: theme.zIndex.drawer + 1,
    flex: '0 0 auto',
}));

export default function PrevPageFrame({
    children,
    text,
    href,
}) {
    return (
        <Box sx={{ height: '100dvh', display: 'flex', flexDirection: 'column' }}>
            <StyledAppBar>
                <Toolbar
                    variant="dense"
                    disableGutters
                    sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        width: '100%',
                        p: '8px 12px',
                    }}
                >
                    <Button
                        variant="text"
                        size="small"
                        aria-label="Back to templates"
                        startIcon={<ArrowBackRoundedIcon />}
                        component="a"
                        href={href ? href : '/'}
                        sx={{ display: { xs: 'none', sm: 'flex' } }}
                    >
                        {text ? text : 'Back'}
                    </Button>
                    <IconButton
                        size="small"
                        aria-label="Back to templates"
                        component="a"
                        href={href ? href : '/'}
                        sx={{ display: { xs: 'auto', sm: 'none' } }}
                    >
                        <ArrowBackRoundedIcon />
                    </IconButton>
                </Toolbar>
            </StyledAppBar>
            <Box sx={{ flex: 'flex', overflow: 'auto', height: '100%' }}>{children}</Box>
        </Box>
    );
}
