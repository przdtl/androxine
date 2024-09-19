import * as React from 'react';

import { useTranslation } from "react-i18next";

import Box from '@mui/material/Box';
import Grid2 from '@mui/material/Grid2';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import { styled } from '@mui/material/styles';
import IconButton from '@mui/material/IconButton';
import ArrowBackRoundedIcon from '@mui/icons-material/ArrowBackRounded';

import LanguageSelect from './LanguageSelect';
import { ColorSchemeTabsBasic } from './ColorModeSwitch';

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
    const { t } = useTranslation();

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
                    <Box sx={{ mr: 0.5 }}>
                        <Button
                            variant="text"
                            size="small"
                            aria-label="Back to templates"
                            startIcon={<ArrowBackRoundedIcon />}
                            component="a"
                            href={href ? href : '/'}
                            sx={{ display: { xs: 'none', sm: 'flex' } }}
                        >
                            {text ? text : t('prev_page.text')}
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
                    </Box>
                    <Grid2 container spacing={0.5} sx={{ ml: 0.5, maxWidth: { xs: '150px', sm: '100%' } }}>
                        <Grid2 size={{ sm: 'auto', xs: 12 }}>
                            <LanguageSelect />
                        </Grid2>
                        <Grid2 size={{ sm: 'auto', xs: 12 }}>
                            <ColorSchemeTabsBasic />
                        </Grid2>
                    </Grid2>
                </Toolbar>
            </StyledAppBar>
            <Box sx={{ flex: 'flex', overflow: 'auto', height: '100%' }}>{children}</Box>
        </Box>
    );
}
