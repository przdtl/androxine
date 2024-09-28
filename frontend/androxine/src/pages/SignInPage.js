import axios from 'axios'

import * as React from 'react';

import { useNavigate } from 'react-router-dom';

import { useTranslation } from "react-i18next";

import { useSnackbar } from 'notistack'

import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';

import PrevPageFrame from '../components/PrevPageFrame';
import GoogleConnect from '../components/GoogleConnect';
import PasswordInput from '../components/inputs/PasswordInput';
import EmailLoginInput from '../components/inputs/EmailLoginInput';
import { PageCard, PageCardContainer } from '../components/PageCard';

import { useAuth } from '../AuthProvider';


export default function SignInPage() {
    const [emailLoginResponseErrorMessages, setEmailLoginResponseErrorMessages] = React.useState([]);
    const [passwordResponseErrorMessages, setPasswordResponseErrorMessages] = React.useState([]);

    const { enqueueSnackbar } = useSnackbar();
    const { login } = useAuth();
    const { i18n, t } = useTranslation();

    let navigate = useNavigate();

    function handleSubmit(event) {
        event.preventDefault();
        const form_data = new FormData(event.currentTarget);
        axios.post(process.env.REACT_APP_BACKEND_API_URL + 'auth/signin/', form_data, {
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
                "Accept-Language": i18n.language,
            },
        })
            .then(response => {
                console.log(response.data);
                console.log(response.status);
                setEmailLoginResponseErrorMessages([]);
                setPasswordResponseErrorMessages([]);

                login(response.data);

                event.target.reset();
                navigate('/home');
            })
            .catch(error => {
                enqueueSnackbar(t('signin.alerts.warning.errors_when_logging_in'), {
                    variant: 'warning',
                    preventDuplicate: true,
                });
                if (!error.response) {
                    return;
                }
                if (error.response.status === 400) {
                    const response_data = error.response.data;
                    setEmailLoginResponseErrorMessages(response_data['username'] || []);
                    setPasswordResponseErrorMessages(response_data['password'] || []);
                }
                else {
                    setEmailLoginResponseErrorMessages([]);
                    setPasswordResponseErrorMessages([]);
                }
            });
    };

    return (
        <>
            <PrevPageFrame href='/home'>
                <PageCardContainer direction="column" justifyContent="space-between">
                    <PageCard variant="outlined">
                        <Typography
                            component="h1"
                            variant="h4"
                            sx={{ width: '100%' }}
                        >
                            {t('signin.header')}
                        </Typography>
                        <Box
                            component="form"
                            onSubmit={handleSubmit}
                            noValidate
                            sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                width: '100%',
                                gap: 2,
                            }}
                        >
                            <EmailLoginInput responseError={emailLoginResponseErrorMessages} />
                            <PasswordInput responseError={passwordResponseErrorMessages} notUseValidators />
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                            >
                                {t('signin.submit_button')}
                            </Button>
                            <Typography sx={{ textAlign: 'center' }}>
                                {t('signin.dont_have_account') + ' '}
                                <span>
                                    <Link
                                        href="/sign-up/"
                                        variant="body2"
                                        sx={{ alignSelf: 'center' }}
                                    >
                                        {t('signin.signup')}
                                    </Link>
                                </span>
                            </Typography>
                        </Box>
                        <Divider>{t('signin.or')}</Divider>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                            <GoogleConnect type='submit'>
                                {t('signin.signin_with_google')}
                            </GoogleConnect>
                        </Box>
                    </PageCard>
                </PageCardContainer>
            </PrevPageFrame>
        </>
    );
}