import * as React from 'react';

import { useTranslation } from "react-i18next";

import FormControl from '@mui/material/FormControl';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputAdornment from '@mui/material/InputAdornment';
import SearchRoundedIcon from '@mui/icons-material/SearchRounded';

export default function Search({
  value,
  handleChange = () => { },
}) {
  const { t } = useTranslation();

  return (
    <FormControl sx={{ width: '100%', height: '100%' }} variant="outlined" >
      <OutlinedInput
        value={value}
        onChange={handleChange}
        size="small"
        id="search"
        placeholder={t('inputs.search.placeholder')}
        sx={{ flexGrow: 1 }}
        startAdornment={<InputAdornment position="start" sx={{ color: 'text.primary' }} />}
      // inputProps={{
      //   'aria-label': 'search',
      // }}
      />
    </FormControl >
  );
}
