import { useTranslation } from "react-i18next";

import './NotFoundPage.css';

export default function NotFoundPage() {
    const { t } = useTranslation();

    return (
        <div id="notfound">
            <div class="notfound">
                <div class="notfound-404"></div>
                <h1>404</h1>
                <h2>{t('404_page.header')}</h2>
                <p>{t('404_page.text')}</p>
                <a href="/home">{t('404_page.back_to_homepage')}</a>
            </div>
        </div>
    );
}