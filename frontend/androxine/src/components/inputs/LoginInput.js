import * as React from 'react';

import { useTranslation } from "react-i18next";

import FormLabel from '@mui/material/FormLabel';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';


export default function LoginInput({
    label,
    responseErrors,
    setValidationError,
    name = 'username',
    id = 'login_input',
}) {
    const [loginErrorMessage, setLoginErrorMessage] = React.useState('');
    const { t } = useTranslation();

    function getErrorMessage(login) {
        if (!login.value) {
            return t('inputs.login.validation.empty');
        }
    }

    const validateLogin = () => {
        const login = document.getElementById(id);
        let msg = getErrorMessage(login);

        setValidationError(msg ? true : false);
        setLoginErrorMessage(msg);
    };

    return (
        < FormControl >
            <FormLabel htmlFor={id}>
                {label ? label : t('inputs.login.label')}
            </FormLabel>
            <TextField
                required
                fullWidth
                id={id}
                name={name}
                placeholder="yourlogin"
                error={Boolean(loginErrorMessage || responseErrors)}
                color={Boolean(loginErrorMessage || responseErrors) ? 'error' : 'primary'}
                onChange={validateLogin}
                helperText={
                    <>
                        {loginErrorMessage && <FormHelperText>{loginErrorMessage}</FormHelperText>}
                        {responseErrors?.map((item) => {
                            return <FormHelperText>{item}</FormHelperText>
                        })}
                    </>
                }
            />
        </ FormControl>
    );
};
