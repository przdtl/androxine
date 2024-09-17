import * as React from 'react';

import { useSnackbar } from 'notistack';

import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';


function SnackbarCloseButton({ snackbarKey }) {
    const { closeSnackbar } = useSnackbar();

    return (
        <IconButton onClick={() => closeSnackbar(snackbarKey)} size="small" >
            <CloseIcon fontSize="inherit" />
        </IconButton>
    );
}

export default SnackbarCloseButton;