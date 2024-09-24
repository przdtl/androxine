import * as React from 'react';

import Chip from '@mui/material/Chip';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import { useTheme } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import FormControl from '@mui/material/FormControl';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
        autoFocus: false,
    },
};

export default function MultipleSelectChip({
    text_label,
    value = [],
    items_list = [],
    handleChange = () => { },
    ...props
}) {
    const theme = useTheme();

    return (
        <FormControl sx={{ width: '100%' }} size='medium'>
            <Select
                id="demo-multiple-chip"
                multiple
                displayEmpty
                value={value}
                onChange={handleChange}
                renderValue={(selected) => {
                    return (
                        <>
                            <Chip label={selected.length} sx={{ mx: 1 }} />
                            <Typography>{text_label}</Typography>
                        </>
                    );
                }}
                MenuProps={MenuProps}
                {...props}
            >
                {items_list.map((item) => (
                    <MenuItem
                        key={item.name}
                        value={item.name}
                        style={{ fontWeight: theme.typography.fontWeightRegular }}
                    >
                        {item.name}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
}
