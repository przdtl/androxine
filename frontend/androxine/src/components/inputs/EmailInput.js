import * as React from 'react';

import FormLabel from '@mui/material/FormLabel';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';


function getErrorMessage(email) {
    if (!email.value) {
        return "Email can't be empty.";
    }
    if (!/\S+@\S+\.\S+/.test(email.value)) {
        return "Please enter a valid email address.";
    }
};

export default function EmailInput({
    setValidationError,
    label = 'Email',
    id = 'email_input',
    name = 'email',
    responseErrors,
}) {
    const [emailErrorMessage, setEmailErrorMessage] = React.useState('');

    const validateEmail = () => {
        const email = document.getElementById(id);
        let msg = getErrorMessage(email)

        setValidationError(msg ? true : false);
        setEmailErrorMessage(msg);
    };

    return (
        <FormControl>
            <FormLabel htmlFor={id}>{label}</FormLabel>
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