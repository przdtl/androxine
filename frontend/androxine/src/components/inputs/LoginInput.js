import * as React from 'react';

import FormLabel from '@mui/material/FormLabel';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';

function getErrorMessage(login) {
    if (!login.value) {
        return "Login can't be empty.";
    }
}

export default function LoginInput({
    setValidationError,
    label = 'Login',
    id = 'login_input',
    name = 'username',
    responseErrors,
}) {
    const [loginErrorMessage, setLoginErrorMessage] = React.useState('');

    const validateLogin = () => {
        const login = document.getElementById(id);
        let msg = getErrorMessage(login);

        setValidationError(msg ? true : false);
        setLoginErrorMessage(msg);
    };

    return (
        < FormControl >
            <FormLabel htmlFor={id}>{label}</FormLabel>
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
