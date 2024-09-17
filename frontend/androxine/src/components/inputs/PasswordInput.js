import * as React from 'react';

import FormLabel from '@mui/material/FormLabel';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';

function getErrorMessage(password, lookup_password) {
    if (lookup_password != null) {
        if (password.value !== lookup_password.value) {
            return "Passwords are not equals.";
        }
        return "";
    }

    if (!password.value) {
        return "Password can't be empty.";
    }
    if (!/[a-z]/.test(password.value)) {
        return 'The password must contain lowercase letters.';
    }
    if (!/[A-Z]/.test(password.value)) {
        return 'The password must contain uppercase letters.';
    }
    if (!/\d/.test(password.value)) {
        return 'The password must contain digits.';
    }
    if (!/[^A-Za-z0-9]/.test(password.value)) {
        return 'The password must contain special characters.';
    }
    if (password.value.length < 8) {
        return 'Password must be at least 8 characters long.';
    }
};

export default function PasswordInput({
    setValidationError,
    label = 'Password',
    id = 'password_input',
    name = 'password',
    componentMapId,
    responseErrors,
    notUseValidators = false,
}) {
    const [passwordErrorMessage, setPasswordErrorMessage] = React.useState('');

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
            <FormLabel htmlFor={id}>{label}</FormLabel>
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