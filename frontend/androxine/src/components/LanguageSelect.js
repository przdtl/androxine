import { useTranslation } from "react-i18next";

import Language from '@mui/icons-material/Language';

import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

import { supportedLngs } from '../i18n';

import { useLocale } from "../LocaleProvider";


export default function LanguageSelect() {
    const { i18n } = useTranslation();
    const { setLocaleByI18nCode } = useLocale();

    const handleSelect = (e) => {
        i18n.changeLanguage(e.target.value);
        setLocaleByI18nCode(i18n.language);
    };

    return (
        <Select
            IconComponent={Language}
            labelId="theme-select-label"
            id="theme-select"
            value={i18n.resolvedLanguage}
            label="Design Language"
            onChange={handleSelect}
            sx={{ width: '100%', height: '100%' }}
        >
            {Object.entries(supportedLngs).map(([code, name]) => (
                <MenuItem value={code} key={code}>
                    {name}
                </MenuItem>
            ))}
        </Select>
    );
};