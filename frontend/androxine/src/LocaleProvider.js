import React, { createContext, useContext } from 'react';

import { useTranslation } from "react-i18next";


export const LocaleContext = createContext();

const i18nLangsToMuiLangs = {
    "ru": "ruRU",
    "en": "enUS",
};

export function LocaleProvider({ children }) {
    const { i18n } = useTranslation();
    const [locale, setLocale] = React.useState(i18nLangsToMuiLangs[i18n.language]);

    function setLocaleByI18nCode(lang_code) {
        setLocale(i18nLangsToMuiLangs[lang_code]);
    };

    return (
        <LocaleContext.Provider value={{ locale, setLocaleByI18nCode }}>
            {children}
        </LocaleContext.Provider>
    );
};


export const useLocale = () => {
    return useContext(LocaleContext);
};
