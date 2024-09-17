import axios from 'axios'

import * as React from 'react';

import { useNavigate } from 'react-router-dom';

import { useSnackbar } from 'notistack'

import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';

import PrevPageFrame from '../components/PrevPageFrame';
import GoogleConnect from '../components/GoogleConnect';
import ForgotPassword from '../components/ForgotPassword';
import PasswordInput from '../components/inputs/PasswordInput';
import EmailLoginInput from '../components/inputs/EmailLoginInput';
import { PageCard, PageCardContainer } from '../components/PageCard';

import { useAuth } from '../AuthProvider';


export default function SignInPage() {
    const [emailLoginResponseErrorMessages, setEmailLoginResponseErrorMessages] = React.useState([]);
    const [passwordResponseErrorMessages, setPasswordResponseErrorMessages] = React.useState([]);
    // const [nonFieldResponseError, setNonFieldResponseError] = React.useState([]);

    const { enqueueSnackbar } = useSnackbar();
    const { login, csrfToken } = useAuth();

    let navigate = useNavigate();

    function handleSubmit(event) {
        event.preventDefault();
        const form_data = new FormData(event.currentTarget);
        axios.post('http://127.0.0.1:8000/auth/signin/', form_data, {
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
                // "X-CSRFToken": csrfToken,
            },
        })
            .then(response => {
                console.log(response.data);
                console.log(response.status);
                setEmailLoginResponseErrorMessages([]);
                setPasswordResponseErrorMessages([]);
                // setNonFieldResponseErrorMessages([]);

                login(response.data);

                event.target.reset();
                navigate('/home');
            })
            .catch(error => {
                enqueueSnackbar('Появились ошибки при входе!', {
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
                    // setNonFieldResponseErrorMessages(response_data['non_field_errors'] || []);
                }
                else {
                    setEmailLoginResponseErrorMessages([]);
                    setPasswordResponseErrorMessages([]);
                    // setNonFieldResponseErrorMessages([]);
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
                            Sign in
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
                            {/* <ForgotPassword open={open} handleClose={handleClose} /> */}
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                            // onClick={validateInputs}
                            >
                                Sign in
                            </Button>
                            <Typography sx={{ textAlign: 'center' }}>
                                Don&apos;t have an account?{' '}
                                <span>
                                    <Link
                                        href="/sign-up/"
                                        variant="body2"
                                        sx={{ alignSelf: 'center' }}
                                    >
                                        Sign up
                                    </Link>
                                </span>
                            </Typography>
                        </Box>
                        <Divider>or</Divider>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                            <GoogleConnect type='submit'>
                                Sign in with Google
                            </GoogleConnect>
                        </Box>
                    </PageCard>
                </PageCardContainer>
            </PrevPageFrame>
        </>
    );
}