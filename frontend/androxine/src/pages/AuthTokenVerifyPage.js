
import axios from 'axios'

import * as React from 'react';

import { useSearchParams } from 'react-router-dom'

import { useTranslation } from 'react-i18next';

import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import Skeleton from '@mui/material/Skeleton';
import Typography from '@mui/material/Typography';

import ErrorIcon from '@mui/icons-material/Error';
import VerifiedIcon from '@mui/icons-material/Verified';

import PrevPageFrame from '../components/PrevPageFrame';
import { PageCard, PageCardContainer } from '../components/PageCard';


export const AuthTokenVerifyPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [isPageLoad, setPageLoad] = React.useState(false);
    const [isEmailVerified, setEmailVerified] = React.useState(false);
    const { t } = useTranslation();

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
                        : (
                            <PageCard variant="outlined">
                                <Stack direction="row" alignItems="center" gap={1}>
                                    {isEmailVerified
                                        ? <VerifiedIcon color='success' />
                                        : <ErrorIcon color='error' />
                                    }
                                    <Typography
                                        variant="body1"
                                        sx={{ width: '100%' }}
                                    >
                                        {isEmailVerified
                                            ? t('email_verify.success_verify.text')
                                            : t('email_verify.unsuccess_verify.text')
                                        }
                                    </Typography>
                                </Stack>
                                {isEmailVerified
                                    ? (
                                        <Link
                                            href="/sign-in/"
                                            variant="body2"
                                        >
                                            {t('email_verify.success_verify.additional_text')}
                                        </Link>
                                    )
                                    : ""
                                }
                            </PageCard>
                        )
                    }
                </PageCardContainer>
            </PrevPageFrame >
        </>
    );
}