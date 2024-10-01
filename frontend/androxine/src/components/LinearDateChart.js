import 'chartjs-adapter-luxon';
import { DateTime } from 'luxon';
import zoomPlugin from 'chartjs-plugin-zoom';

import { Chart } from 'react-chartjs-2';

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

let options = {
    maintainAspectRatio: false,
    interaction: {
        intersect: false,
        mode: 'index',
    },
    scales: {
        y: {
            beginAtZero: true,
        },
        x: {
            type: 'time',
            time: {
                unit: 'day'
            },
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
        },
    },
};


export default function LinearDateChart({
    data,
}) {
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