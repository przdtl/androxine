import * as React from 'react';

import { useTranslation } from "react-i18next";

import FormLabel from '@mui/material/FormLabel';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';


export default function PasswordInput({
    label,
    componentMapId,
    responseErrors,
    setValidationError,
    name = 'password',
    id = 'password_input',
    notUseValidators = false,
}) {
    const [passwordErrorMessage, setPasswordErrorMessage] = React.useState('');
    const { t } = useTranslation();

    function getErrorMessage(password, lookup_password) {
        if (lookup_password != null) {
            if (password.value !== lookup_password.value) {
                return t('inputs.password.validation.equality');
            }
            return "";
        }

        if (!password.value) {
            return t('inputs.password.validation.empty');
        }
        if (!/[a-z]/.test(password.value)) {
            return t('inputs.password.validation.lowercase_letters');
        }
        if (!/[A-Z]/.test(password.value)) {
            return t('inputs.password.validation.uppercase_letters');
        }
        if (!/\d/.test(password.value)) {
            return t('inputs.password.validation.digits');
        }
        if (!/[^A-Za-z0-9]/.test(password.value)) {
            return t('inputs.password.validation.special_characters');
        }
        if (password.value.length < 8) {
            return t('inputs.password.validation.length');
        }
    };

    const validatePassword = () => {
        const password = document.getElementById(id);
        const lookup_password = document.getElementById(componentMapId);

        let msg = getErrorMessage(password, lookup_password);

        if (notUseValidators) {
            return;
        }

        setValidationError(msg ? true : false);
        setPasswordErrorMessage(msg);
    };

    return (
        <FormControl>
            <FormLabel htmlFor={id}>
                {label ? label : t('inputs.password.label')}
            </FormLabel>
            <TextField
                required
                fullWidth
                placeholder="••••••••••••"
                type="password"
                name={name}
                id={id}
                variant="outlined"
                error={Boolean(passwordErrorMessage || responseErrors)}
                color={Boolean(passwordErrorMessage || responseErrors) ? 'error' : 'primary'}
                onChange={validatePassword}
                helperText={
                    <>
                        {passwordErrorMessage && <FormHelperText>{passwordErrorMessage}</FormHelperText>}
                        {!notUseValidators && responseErrors?.map((item) => {
                            return <FormHelperText>{item}</FormHelperText>
                        })}
                    </>
                }
            />
        </FormControl>
    );
};