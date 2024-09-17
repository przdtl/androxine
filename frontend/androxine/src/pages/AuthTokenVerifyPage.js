
import axios from 'axios'

import * as React from 'react';

import { useSearchParams } from 'react-router-dom'

import Skeleton from '@mui/material/Skeleton';
import Typography from '@mui/material/Typography';

import PrevPageFrame from '../components/PrevPageFrame';
import { PageCard, PageCardContainer } from '../components/PageCard';


export const AuthTokenVerifyPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [isPageLoad, setPageLoad] = React.useState(false);
    const [isEmailVerified, setEmailVerified] = React.useState(false);

    const user_id = searchParams.get('user_id');
    const token = searchParams.get('token');

    function activateAccount() {
        axios.get(`http://127.0.0.1:8000/auth/activate/${user_id}/${token}`)
            .then(response => {
                console.log(response.data);
                console.log(response.status);

                if (response.ok) {
                    setEmailVerified(true);
                }
            })
            .catch(error => {
                if (!error.response) {
                    return;
                }
                console.log(error.response.data);
                console.log(error.response.status);
                if (error.response.status === 400) {
                    setEmailVerified(true);
                }
            })
            .finally(() => {
                setPageLoad(true);
            });
    };

    React.useEffect(() => {
        activateAccount();
    }, [])


    return (
        <>
            <PrevPageFrame href='/home' >
                <PageCardContainer direction="column" justifyContent="start" >
                    {!isPageLoad
                        ?
                        <PageCard>
                            <Skeleton variant="rounded" />
                        </PageCard>
                        : isEmailVerified
                            ?
                            <PageCard variant="outlined">
                                <Typography
                                    component="h1"
                                    variant="h4"
                                    sx={{ width: '100%' }}
                                >
                                    The email address has been successfully verified
                                </Typography>
                            </PageCard>
                            :
                            <PageCard>
                                <Typography
                                    component="h1"
                                    variant="h4"
                                    sx={{ width: '100%' }}
                                >
                                    An error occurred while confirming the email address
                                </Typography>
                            </PageCard>
                    }
                </PageCardContainer>
            </PrevPageFrame >
        </>
    );
}