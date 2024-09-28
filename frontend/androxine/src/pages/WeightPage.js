import React, { useState } from 'react';

import axios from 'axios';

import colorLib from '@kurkle/color';

import zoomPlugin from 'chartjs-plugin-zoom';

import {
    Chart as ChartJS,
    LinearScale,
    CategoryScale,
    BarElement,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
} from 'chart.js';

import {
    Chart,
} from 'react-chartjs-2';

import Box from '@mui/material/Box';
import { Button, FormControl, FormLabel, Grid2, Stack, TextField } from '@mui/material';

ChartJS.register(
    LinearScale,
    CategoryScale,
    BarElement,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    zoomPlugin,
);

export const options = {
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
            max: 30,
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
                mode: 'xy',
            },
            limits: {
                x: { minRange: 5 },
                y: { min: 0, max: 150, minRange: 10 }
            },
        },

    },
};

const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'January', 'February', 'March', 'April', 'May', 'June', 'July'];




export default function WeightPage() {
    const [startWeight, setStartWeight] = useState(68);
    const [desiredWeight, setDesiredWeight] = useState(80);
    const [weightLabels, setWeightLabels] = useState([]);
    const [weightData, setWeightData] = useState([]);
    const [weightResponse, setWeightResponse] = useState({});

    const handleGetWeight = () => {
        axios({
            url: '',
            method: 'get',

        })
            .then(response => {
                const data = response.data;
            })
            .catch(error => {

            });
    };

    const convertWeightResponseToChartData = (data) => {

    };

    const data = {
        labels,
        datasets: [
            {
                type: 'line',
                label: 'Weight',
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: colorLib('rgb(255, 99, 132)').alpha(0.5).rgbString(),
                tension: 0.2,
                pointStyle: 'circle',
                pointRadius: 2,
                pointHoverRadius: 5,
                fill: true,
                data: labels.map(() => Math.floor(Math.random() * (80 - 70) + 70)),
            },
            {
                type: 'line',
                label: 'Start',
                borderColor: 'rgb(75, 192, 192)',
                borderDash: [5, 5],
                borderWidth: 2,
                pointStyle: false,
                data: labels.map(() => startWeight),
            },
            {
                type: 'line',
                label: 'Goal',
                borderColor: 'rgb(54, 162, 235)',
                borderDash: [5, 5],
                borderWidth: 2,
                pointStyle: false,
                data: labels.map(() => desiredWeight),
            },
        ],
    };

    return (
        <>
            <Grid2 container spacing={2} columns={12}>
                <Grid2 size={{ md: 12, lg: 9 }}>
                    <Box style={{ height: "60vh", position: "relative" }}>
                        <Chart
                            type='bar'
                            options={options}
                            data={data}
                        />
                    </Box>
                </Grid2>
                <Grid2 size={{ xs: 12, lg: 3 }}>
                    <Stack gap={2} direction={{ xs: 'column', sm: 'row', lg: 'column' }} sx={{ alignItems: { xs: 'normal', sm: 'end', lg: 'normal' } }}>
                        <FormControl>
                            <FormLabel>
                                Стартовый вес
                            </FormLabel>
                            <TextField variant="outlined" onChange={event => setStartWeight(event.target.value)} value={startWeight} />
                        </FormControl>
                        <FormControl>
                            <FormLabel>
                                Желанный вес
                            </FormLabel>
                            <TextField variant="outlined" onChange={event => setDesiredWeight(event.target.value)} value={desiredWeight} />
                        </FormControl>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                        >
                            Сохранить
                        </Button>
                    </Stack>
                </Grid2>
            </Grid2>

        </>
    );
}
