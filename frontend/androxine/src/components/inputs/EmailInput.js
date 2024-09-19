import * as React from 'react';

import { useTranslation } from "react-i18next";

import FormLabel from '@mui/material/FormLabel';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';


export default function EmailInput({
    label,
    responseErrors,
    setValidationError,
    name = 'email',
    id = 'email_input',
}) {
    const [emailErrorMessage, setEmailErrorMessage] = React.useState('');
    const { t } = useTranslation();

    function getErrorMessage(email) {
        if (!email.value) {
            return t('inputs.email.validation.empty');
        }
        if (!/\S+@\S+\.\S+/.test(email.value)) {
            return t('inputs.email.validation.invalid');
        }
    };

    const validateEmail = () => {
        const email = document.getElementById(id);
        let msg = getErrorMessage(email)

        setValidationError(msg ? true : false);
        setEmailErrorMessage(msg);
    };

    return (
        <FormControl>
            <FormLabel htmlFor={id}>
                {label ? label : t('inputs.email.label')}
            </FormLabel>
            <TextField
                id={id}
                name={name}
                type="email"
                placeholder="your@email.com"
                required
                fullWidth
                variant="outlined"
                onChange={validateEmail}
                error={Boolean(emailErrorMessage || responseErrors)}
                color={Boolean(emailErrorMessage || responseErrors) ? 'error' : 'primary'}
                helperText={
                    <>
                        {emailErrorMessage && <FormHelperText>{emailErrorMessage}</FormHelperText>}
                        {responseErrors.map((item) => {
                            return <FormHelperText>{item}</FormHelperText>
                        })}
                    </>
                }
            />
        </FormControl>
    );
};