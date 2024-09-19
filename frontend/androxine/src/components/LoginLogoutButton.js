import axios from 'axios';

import { useSnackbar } from 'notistack';

import { useTranslation } from "react-i18next";

import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import LoginRoundedIcon from '@mui/icons-material/LoginRounded';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';

import { useAuth } from '../AuthProvider';


export default function LoginLogoutButton({

}) {
    const { isAuth, logout, csrfToken, getCSRF } = useAuth();
    const { enqueueSnackbar } = useSnackbar();
    const { t } = useTranslation();

    function handleLogout() {
        axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/auth/signout/',
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
        })
            .then(response => {
                console.log(response);
                logout();
                getCSRF();
            })
            .catch(error => {
                console.log(error);
                enqueueSnackbar(t('signout.alerts.warning.logout_error'), {
                    variant: 'warning',
                    preventDuplicate: true,
                });
            });
    };

    return (
        <Button
            variant="outlined"
            fullWidth startIcon={isAuth ? <LogoutRoundedIcon /> : <LoginRoundedIcon />}
            {...(isAuth ? { onClick: handleLogout } : { href: '/sign-in' })}
        >
            <Typography variant='body1'>
                {isAuth ? t("menu_content.logout") : t("menu_content.login")}
            </Typography>
        </Button>
    );
}