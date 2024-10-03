import 'chartjs-adapter-luxon';
import { DateTime, Interval } from 'luxon';

import zoomPlugin from 'chartjs-plugin-zoom';

import { Chart } from 'react-chartjs-2';

import { useTranslation } from "react-i18next";

import Box from '@mui/material/Box';

import {
    Chart as ChartJS,
    LinearScale,
    CategoryScale,
    BarElement,
    PointElement,
    LineElement,
    Filler,
    TimeScale,
    Tooltip,
} from 'chart.js';


ChartJS.register(
    LinearScale,
    CategoryScale,
    TimeScale,
    BarElement,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    zoomPlugin,
);


export default function LinearDateChart({
    data,
    x_zoom_max,
    x_zoom_min,
}) {
    const { i18n } = useTranslation();

    const one_day_interval = Interval.fromDateTimes(DateTime.now(), DateTime.now().plus({ days: 2 })).toDuration();
    let options = {
        locale: i18n.language,
        maintainAspectRatio: false,
        interaction: {
            intersect: false,
            mode: 'index',
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    display: false,
                }
            },
            x: {
                type: 'time',
                time: {
                    unit: 'day',
                    tooltipFormat: 'DD',
                },
                min: x_zoom_min,
                max: x_zoom_max,
                grid: {
                    display: false,
                }
            },
        },
        plugins: {
            zoom: {
                zoom: {
                    wheel: {
                        enabled: true,
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'x',
                },
                pan: {
                    enabled: true,
                    mode: 'x',
                },
                limits: {
                    x: {
                        min: x_zoom_min,
                        max: x_zoom_max,
                        minRange: one_day_interval,
                    },
                },
            },
        },
    };


    return (
        <Box style={{ height: "60vh", position: "relative" }}>
            <Chart
                type='line'
                options={options}
                data={data}
            />
        </Box>
    );
};