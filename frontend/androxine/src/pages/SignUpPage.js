import axios from 'axios'

import * as React from 'react';

import { useTranslation } from "react-i18next";

import { useSnackbar } from 'notistack'

import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';

import PrevPageFrame from '../components/PrevPageFrame';
import GoogleConnect from '../components/GoogleConnect';
import EmailInput from '../components/inputs/EmailInput';
import LoginInput from '../components/inputs/LoginInput';
import PasswordInput from '../components/inputs/PasswordInput';
import { PageCard, PageCardContainer } from '../components/PageCard';
import i18n from '../i18n';


export default function SignUpPage() {
    const [emailResponseErrorMessages, setEmailResponseErrorMessages] = React.useState([]);
    const [loginResponseErrorMessages, setLoginResponseErrorMessages] = React.useState([]);
    const [passwordResponseErrorMessages, setPasswordResponseErrorMessages] = React.useState([]);

    const [isEmailValidationError, setEmailValidationError] = React.useState(false);
    const [isLoginValidationError, setLoginValidationError] = React.useState(false);
    const [isPasswordValidationError, setPasswordValidationError] = React.useState(false);
    const [isPasswordRepeatValidationError, setPasswordRepeatValidationError] = React.useState(false);

    const { enqueueSnackbar } = useSnackbar();
    const { i18n, t } = useTranslation();

    function handleSubmit(event) {
        event.preventDefault();
        if (isEmailValidationError || isLoginValidationError || isPasswordValidationError || isPasswordRepeatValidationError) {
            return;
        }
        const form_data = new FormData(event.currentTarget);
        axios.post(process.env.REACT_APP_BACKEND_API_URL + 'auth/signup/', form_data, {
            headers: {
                "Accept-Language": i18n.language,
            }
        })
            .then(response => {
                console.log(response.data);
                console.log(response.status);
                setLoginResponseErrorMessages([]);
                setEmailResponseErrorMessages([]);
                setPasswordResponseErrorMessages([]);

                event.target.reset();

                enqueueSnackbar(t('signup.alerts.info.email_has_been_sent'), {
                    variant: 'info',
                    preventDuplicate: true,
                }
                );
            })
            .catch(error => {
                if (!error.response) {
                    return;
                }
                if (error.response.status === 400) {
                    const response_data = error.response.data;
                    setLoginResponseErrorMessages(response_data['username'] || []);
                    setEmailResponseErrorMessages(response_data['email'] || []);
                    setPasswordResponseErrorMessages(response_data['password'] || []);
                }
                else {
                    setLoginResponseErrorMessages([]);
                    setEmailResponseErrorMessages([]);
                    setPasswordResponseErrorMessages([]);
                }
                enqueueSnackbar(t('signup.alerts.warning.errors_during_registration'), {
                    variant: 'warning',
                    preventDuplicate: true,
                });
            });
    };

    return (
        <>
            <PrevPageFrame href='/home'>
                <PageCardContainer direction="column" justifyContent="space-between">
                    <Stack
                        sx={{
                            justifyContent: 'center',
                            height: '100dvh',
                            p: 2,
                        }}
                    >
                        <PageCard variant="outlined">
                            <Typography
                                component="h1"
                                variant="h4"
                                sx={{ width: '100%' }}
                            >
                                {t('signup.header')}
                            </Typography>
                            <Box
                                component="form"
                                onSubmit={handleSubmit}
                                sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}
                            >
                                <LoginInput
                                    name='username'
                                    responseErrors={loginResponseErrorMessages}
                                    setValidationError={(value) => { setLoginValidationError(value) }}
                                />
                                <EmailInput
                                    name='email'
                                    responseErrors={emailResponseErrorMessages}
                                    setValidationError={(value) => { setEmailValidationError(value) }} />
                                <PasswordInput
                                    name='password'
                                    id="password1"
                                    responseErrors={passwordResponseErrorMessages}
                                    setValidationError={(value) => { setPasswordValidationError(value) }} />
                                <PasswordInput
                                    name='password2'
                                    label={t('signup.password_repeat_label')}
                                    id="password2"
                                    componentMapId="password1"
                                    setValidationError={(value) => { setPasswordRepeatValidationError(value) }}
                                />
                                <Button
                                    type="submit"
                                    fullWidth
                                    variant="contained"
                                >
                                    {t('signup.submit_button')}
                                </Button>
                                <Typography sx={{ textAlign: 'center' }}>
                                    {t('signup.already_have_account') + ' '}
                                    <span>
                                        <Link
                                            href="/sign-in/"
                                            variant="body2"
                                            sx={{ alignSelf: 'center' }}
                                        >
                                            {t('signup.signin')}
                                        </Link>
                                    </span>
                                </Typography>
                            </Box>
                            <Divider>
                                <Typography sx={{ color: 'text.secondary' }}>
                                    {t('signup.or')}
                                </Typography>
                            </Divider>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                                <GoogleConnect type='submit'>
                                    {t('signup.signin_with_google')}
                                </GoogleConnect>
                            </Box>
                        </PageCard>
                    </Stack>
                </PageCardContainer>
            </PrevPageFrame>
        </>
    );
}
