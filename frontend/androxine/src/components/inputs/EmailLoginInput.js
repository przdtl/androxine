import * as React from 'react';

import FormLabel from '@mui/material/FormLabel';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';


export default function EmailLoginInput({
    label = 'Email/ Login',
    id = 'email_login_input',
    name = 'username',
    responseErrors = [],
}) {

    return (
        < FormControl >
            <FormLabel htmlFor={id}>{label}</FormLabel>
            <TextField
                required
                fullWidth
                id={id}
                name={name}
                placeholder="your@email.com/ yourlogin"
                color={Boolean(responseErrors) ? 'error' : 'primary'}
                helperText={
                    <>
                        {responseErrors.map((item) => {
                            <FormHelperText>{item}</FormHelperText>
                        })}
                    </>
                }
            />
        </ FormControl>
    );
};