import axios from 'axios'

import * as React from 'react';

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

import { useSnackbar } from 'notistack'


export default function SignUpPage() {
    const { enqueueSnackbar } = useSnackbar();

    const [emailResponseErrorMessages, setEmailResponseErrorMessages] = React.useState([]);
    const [loginResponseErrorMessages, setLoginResponseErrorMessages] = React.useState([]);
    const [passwordResponseErrorMessages, setPasswordResponseErrorMessages] = React.useState([]);
    // const [nonFieldResponseErrorMessages, setNonFieldResponseErrorMessages] = React.useState([]);

    const [isEmailValidationError, setEmailValidationError] = React.useState(false);
    const [isLoginValidationError, setLoginValidationError] = React.useState(false);
    const [isPasswordValidationError, setPasswordValidationError] = React.useState(false);
    const [isPasswordRepeatValidationError, setPasswordRepeatValidationError] = React.useState(false);

    function handleSubmit(event) {
        event.preventDefault();
        if (isEmailValidationError || isLoginValidationError || isPasswordValidationError || isPasswordRepeatValidationError) {
            return;
        }
        const form_data = new FormData(event.currentTarget);
        axios.post('http://127.0.0.1:8000/auth/signup/', form_data)
            .then(response => {
                console.log(response.data);
                console.log(response.status);
                setLoginResponseErrorMessages([]);
                setEmailResponseErrorMessages([]);
                setPasswordResponseErrorMessages([]);
                // setNonFieldResponseErrorMessages([]);

                event.target.reset();

                enqueueSnackbar('На указанную почту было отправлено письмо с ссылкой для активации аккаунта.', {
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
                    // setNonFieldResponseErrorMessages(response_data['non_field_errors'] || []);
                }
                else {
                    setLoginResponseErrorMessages([]);
                    setEmailResponseErrorMessages([]);
                    setPasswordResponseErrorMessages([]);
                    // setNonFieldResponseErrorMessages([]);
                }
                enqueueSnackbar('Появились ошибки при регистрации!', {
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
                                Sign up
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
                                    responseErrors={passwordResponseErrorMessages}
                                    setValidationError={(value) => { setPasswordValidationError(value) }} label="Password" id="password1" />
                                <PasswordInput
                                    name='password2'
                                    setValidationError={(value) => { setPasswordRepeatValidationError(value) }}
                                    label="Password repeat"
                                    id="password2"
                                    componentMapId="password1"
                                />
                                <Button
                                    type="submit"
                                    fullWidth
                                    variant="contained"
                                >
                                    Sign up
                                </Button>
                                <Typography sx={{ textAlign: 'center' }}>
                                    Already have an account?{' '}
                                    <span>
                                        <Link
                                            href="/sign-in/"
                                            variant="body2"
                                            sx={{ alignSelf: 'center' }}
                                        >
                                            Sign in
                                        </Link>
                                    </span>
                                </Typography>
                            </Box>
                            <Divider>
                                <Typography sx={{ color: 'text.secondary' }}>or</Typography>
                            </Divider>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                                <GoogleConnect type='submit'>
                                    Sign up with Google
                                </GoogleConnect>
                            </Box>
                        </PageCard>
                    </Stack>
                </PageCardContainer>
            </PrevPageFrame>
        </>
    );
}
