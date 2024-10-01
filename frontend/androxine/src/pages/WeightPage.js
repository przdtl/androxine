import React, { useEffect, useRef, useState } from 'react';

import axios from 'axios';

import colorLib from '@kurkle/color';

import { useSnackbar } from 'notistack'

import { DateTime } from 'luxon';

import { useTranslation } from "react-i18next";

import { styled, useTheme } from '@mui/material/styles';

import Table from '@mui/material/Table';
import Stack from '@mui/material/Stack';
import Paper from '@mui/material/Paper';
import Grid2 from '@mui/material/Grid2';
import Dialog from '@mui/material/Dialog';
import Button from '@mui/material/Button';
import TableRow from '@mui/material/TableRow';
import TableBody from '@mui/material/TableBody';
import FormLabel from '@mui/material/FormLabel';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import FormControl from '@mui/material/FormControl';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import TableContainer from '@mui/material/TableContainer';
import Divider, { dividerClasses } from '@mui/material/Divider';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';

import dayjs from 'dayjs';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterLuxon } from '@mui/x-date-pickers/AdapterLuxon';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

import AddIcon from '@mui/icons-material/Add';
import SyncIcon from '@mui/icons-material/Sync';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import RemoveIcon from '@mui/icons-material/Remove';
import ArrowDropUpIcon from '@mui/icons-material/ArrowDropUp';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';

import { useAuth } from '../AuthProvider';

import LinearDateChart from '../components/LinearDateChart';
import TopBottomPagination from '../components/TopBottomPagination';
import { MobileDatePicker } from '@mui/x-date-pickers/MobileDatePicker';


const MAX_WEIGHT_CHART_VALUE = 200;
const MIN_WEIGHT_CHART_VALUE = 0;

function CreateWeightDialog({
    open,
    weightDate,
    weightValue,
    weightDescription,
    handleChangeWeightDate,
    handleChangeWeightValue,
    handleChangeWeightDescription,
    handleClose,
    handleSubmit,
}) {
    const { i18n, t } = useTranslation();

    return (
        <Dialog
            open={open}
            onClose={handleClose}
            PaperProps={{
                component: 'form',
                onSubmit: handleSubmit,
            }}
        >
            <DialogTitle>
            </DialogTitle>
            <DialogContent>
                <Stack spacing={1}>
                    <Stack spacing={1}>
                        <FormLabel>Дата</FormLabel>
                        <LocalizationProvider dateAdapter={AdapterLuxon} adapterLocale={i18n.language}>
                            <MobileDatePicker
                                maxDate={DateTime.now()}
                                defaultValue={DateTime.now()}
                                name='date'
                                value={weightDate}
                                onChange={handleChangeWeightDate}
                            />
                        </LocalizationProvider>
                    </Stack>
                    <FormControl>
                        <FormLabel>Вес</FormLabel>
                        <TextField
                            fullWidth
                            name='body_weight'
                            type='number'
                            value={weightValue}
                            onChange={handleChangeWeightValue}
                        />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Описание</FormLabel>
                        <TextField
                            fullWidth
                            multiline
                            rows={5}
                            name='description'
                            value={weightDescription}
                            onChange={handleChangeWeightDescription}
                        />
                    </FormControl>
                </Stack>
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose}>Закрыть</Button>
                <Button
                    type="submit"
                >
                    Добавить</Button>
            </DialogActions>
        </Dialog>
    );
};

function ChangeWeightDialog({
    open,
    weightObject,
    weightValue,
    weightDescription,
    handleChangeWeightValue,
    handleChangeWeightDescription,
    handleClose,
    handleSubmit,
    handleDelete,
}) {
    return (
        <Dialog
            open={open}
            onClose={handleClose}
            PaperProps={{
                component: 'form',
                onSubmit: (event) => handleSubmit(event, weightObject.id),
            }}
        >
            <DialogTitle>{DateTime.fromISO(weightObject.date).toLocaleString()}</DialogTitle>
            <DialogContent>
                <Stack spacing={1}>
                    <FormControl>
                        <FormLabel>Вес</FormLabel>
                        <TextField
                            fullWidth
                            name='body_weight'
                            type='number'
                            value={weightValue}
                            onChange={handleChangeWeightValue}
                        />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Описание</FormLabel>
                        <TextField
                            fullWidth
                            multiline
                            rows={5}
                            name='description'
                            value={weightDescription}
                            onChange={handleChangeWeightDescription}
                        />
                    </FormControl>
                </Stack>
            </DialogContent>
            <DialogActions>
                <IconButton size='small' onClick={() => handleDelete(weightObject.id)}>
                    <DeleteIcon color='error' fontSize='small' />
                </IconButton>
                <Button onClick={handleClose}>Закрыть</Button>
                <Button
                    type="submit"
                    {...(weightObject.body_weight == weightValue && weightObject.description == weightDescription ? { disabled: true } : {})}
                >
                    Сохранить</Button>
            </DialogActions>
        </Dialog>
    );
};

export default function WeightPage() {
    // chart started and desired value states
    const [dynamicStartedWeight, setDynamicStartedWeight] = useState();
    const [dynamicDesiredWeight, setDynamicDesiredWeight] = useState();
    const [staticStartedWeight, setStaticStartedWeight] = useState();
    const [staticDesiredWeight, setStaticDesiredWeight] = useState();

    // weight list page states
    const [weightPageCount, setWeightPageCount] = React.useState(1);
    const [weightCurrentPage, setWeightCurrentPage] = React.useState(1);
    const [weightNextPage, setWeightNextPage] = React.useState(null);
    const [isOverwriteWeights, setIsOverwriteWights] = React.useState(true);

    const [userWeightSettingsIsPresent, setUserWeightSettingsIsPresent] = useState(false);
    const [weightLabels, setWeightLabels] = useState([]);
    const [weightTableData, setWeightTableData] = useState([]);
    const [weightList, setWeightList] = useState([]);

    // change weight record states
    const [isUpdateDialogOpen, setIsUpdateDialogOpen] = useState(false);
    const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
    const [changableWeightDateInput, setChangableWeightDateInput] = useState();
    const [changableWeightValueInput, setChangableWeightValueInput] = useState();
    const [changableWeightDescriptionInput, setChangableWeightDescriptionInput] = useState();
    const [changableWeightRecord, setChangableWeightRecord] = useState({});


    const { csrfToken } = useAuth();

    const { enqueueSnackbar } = useSnackbar();
    const { i18n, t } = useTranslation();

    const theme = useTheme();

    const handleOpenUpdateDialog = (weight_record) => {
        setChangableWeightValueInput(weight_record.body_weight);
        setChangableWeightDescriptionInput(weight_record.description);
        setChangableWeightRecord(weight_record);
        setIsUpdateDialogOpen(true);
    };

    const handleCloseUpdateDialog = () => {
        setIsUpdateDialogOpen(false);
        setChangableWeightValueInput();
        setChangableWeightDescriptionInput();
        setChangableWeightRecord({});
    };

    const handleCloseCreateDialog = (e) => {
        setIsCreateDialogOpen(false);
        setChangableWeightDateInput();
        setChangableWeightValueInput();
        setChangableWeightDescriptionInput();
    };

    const handleOpenCreateDialog = () => {
        setIsCreateDialogOpen(true);
        setChangableWeightDateInput();
        setChangableWeightValueInput()
        setChangableWeightDescriptionInput();
    };

    const handleDeleteWeightRecord = (weight_record_id) => {
        axios({
            url: process.env.REACT_APP_BACKEND_API_URL + `weight/${weight_record_id}/`,
            method: 'delete',
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                "Accept-Language": i18n.language,
            },
        })
            .then(response => {
                handleCloseUpdateDialog();
                handleGetWeight();
                handleGetTableWeight();
            })
            .catch(error => {

            });
    };

    const handleUpdateWeightRecord = (event, weight_record_id) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        axios({
            url: process.env.REACT_APP_BACKEND_API_URL + `weight/${weight_record_id}/`,
            method: 'patch',
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                "Accept-Language": i18n.language,
            },
            data: formData,
        })
            .then(response => {
                handleCloseUpdateDialog();
                handleGetWeight();
                handleGetTableWeight();
            })
            .catch(error => {

            });
    };

    const handleCreateWeightRecord = (event) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const formJson = Object.fromEntries(formData.entries());
        formJson.date = changableWeightDateInput.toISODate();
        axios({
            url: process.env.REACT_APP_BACKEND_API_URL + 'weight/',
            method: 'post',
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                "Accept-Language": i18n.language,
            },
            data: formJson,
        })
            .then(response => {
                handleCloseCreateDialog();
                handleGetWeight();
                handleGetTableWeight();
            })
            .catch(error => {

            });
    }

    const getStripedStyle = (index) => {
        return { backgroundColor: index % 2 ? theme.palette.background.default : theme.palette.action.hover };
    };

    const getDeleteBottomBorderStyle = (condition) => {
        if (condition) {
            return {
                [`& .${tableCellClasses.root}`]: {
                    borderBottom: "none"
                },
            };
        }
        return {};
    }

    const handleSetWorkoutSettings = () => {
        let url = 'weight/settings/me/';
        let method = 'patch';
        if (!userWeightSettingsIsPresent) {
            url = 'weight/settings/';
            method = 'post';
        }
        axios({
            url: process.env.REACT_APP_BACKEND_API_URL + url,
            method: method,
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            data: {
                started_weight: dynamicStartedWeight,
                desired_weight: dynamicDesiredWeight,
            },
        })
            .then(response => {
                setStaticStartedWeight(response.data.started_weight);
                setStaticDesiredWeight(response.data.desired_weight);
                setUserWeightSettingsIsPresent(true);
            })
            .catch(error => {
                setUserWeightSettingsIsPresent(false);
            });
    };

    const handleGetWorkoutSettings = () => {
        axios({
            url: process.env.REACT_APP_BACKEND_API_URL + 'weight/settings/me/',
            method: 'get',
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(response => {
                setStaticStartedWeight(response.data.started_weight);
                setStaticDesiredWeight(response.data.desired_weight);
                setUserWeightSettingsIsPresent(true);
            })
            .catch(error => {
                setStaticStartedWeight();
                setStaticDesiredWeight();
                setUserWeightSettingsIsPresent(false);
            });
    };

    const handleChangeStartedWeight = (event) => {
        let value = parseInt(event.target.value);

        if (value > MAX_WEIGHT_CHART_VALUE) value = MAX_WEIGHT_CHART_VALUE;
        if (value < MIN_WEIGHT_CHART_VALUE) value = MIN_WEIGHT_CHART_VALUE;

        setDynamicStartedWeight(value);
    };

    const handleChangeDesiredWeight = (event) => {
        let value = parseInt(event.target.value);

        if (value > MAX_WEIGHT_CHART_VALUE) value = MAX_WEIGHT_CHART_VALUE;
        if (value < MIN_WEIGHT_CHART_VALUE) value = MIN_WEIGHT_CHART_VALUE;

        setDynamicDesiredWeight(value);
    };

    const handleChangePage = (event, value) => {
        setWeightCurrentPage(value);
    };

    const handleShowMore = () => {
        setIsOverwriteWights(false);
        setWeightCurrentPage(weightCurrentPage + 1);
    };

    const handleResetWorkoutSettings = () => {
        setDynamicStartedWeight(staticStartedWeight);
        setDynamicDesiredWeight(staticDesiredWeight);
    };

    const convertWeightTableResponseDataToChartData = (response_table_data) => {
        return response_table_data.map(value => ({ x: value.date, y: value.body_weight }));
    };

    const handleGetTableWeight = () => {
        axios({
            url: process.env.REACT_APP_BACKEND_API_URL + 'weight/table/',
            method: 'get',
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(response => {
                setWeightLabels(response.data.labels);
                setWeightTableData(convertWeightTableResponseDataToChartData(response.data.values));
            })
            .catch(error => {

            });
    };

    const handleGetWeight = () => {
        axios({
            url: process.env.REACT_APP_BACKEND_API_URL + 'weight/',
            method: 'get',
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(response => {
                setWeightList(response.data.results);
            })
            .catch(error => {
                setWeightList();
            });
    };

    const getWeightTrendingIcon = (index) => {
        if (index === weightList.length - 1 || weightList[index + 1].body_weight === weightList[index].body_weight) {
            return <RemoveIcon />
        }
        if (weightList[index + 1].body_weight > weightList[index].body_weight) {
            return <ArrowDropDownIcon color='error' />
        }
        return <ArrowDropUpIcon color='success' />
    };

    const getWeightTableYearRow = (index) => {
        const current_year = DateTime.fromISO(weightList[index].date).year;
        if (index > 0 && DateTime.fromISO(weightList[index - 1].date).year == current_year) {
            return;
        }
        return (
            <TableRow
                sx={{
                    background: `
                    repeating-linear-gradient(
                        45deg,
                        ${theme.palette.background.default},
                        ${theme.palette.background.default} 10px,
                        ${theme.palette.action.hover} 10px,
                        ${theme.palette.action.hover} 20px
                    );`,
                }}
            >
                <TableCell colSpan={3} align='center'>
                    <Typography>
                        {current_year}
                    </Typography>
                </TableCell>
            </TableRow>
        );
    };

    const getMonthDayDate = (iso_date) => {
        const date = DateTime.fromISO(iso_date);

        return `${date.monthLong} ${date.day}`;
    };

    useEffect(() => {
        handleGetWeight();
        handleGetTableWeight();
        handleGetWorkoutSettings();
    }, []);

    useEffect(() => {
        handleGetWeight();
        handleGetTableWeight();
    }, [weightCurrentPage,]);

    useEffect(() => {
        handleResetWorkoutSettings();
    }, [staticStartedWeight, staticDesiredWeight]);

    const data = {
        weightLabels,
        datasets: [
            {
                type: 'line',
                label: 'Weight',
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: colorLib('rgb(255, 99, 132)').alpha(0.5).rgbString(),
                tension: 0.2,
                pointStyle: 'circle',
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true,
                data: weightTableData,
            },
            {
                type: 'line',
                label: 'Start',
                borderColor: 'rgb(75, 192, 192)',
                borderDash: [5, 5],
                borderWidth: 2,
                pointStyle: false,
                data: weightTableData.map((data) => ({ x: data.x, y: dynamicStartedWeight })),
            },
            {
                type: 'line',
                label: 'Goal',
                borderColor: 'rgb(54, 162, 235)',
                borderDash: [5, 5],
                borderWidth: 2,
                pointStyle: false,
                data: weightLabels.map((data) => ({ x: data, y: dynamicDesiredWeight })),
            },
        ],
    };

    return (
        <>
            <Grid2 container spacing={2} columns={12}>
                <Grid2 size={{ md: 12, lg: 9 }}>
                    <LinearDateChart
                        data={data}
                        x_min_value={weightLabels[0]}
                        x_max_value={weightLabels[weightLabels.length - 1]}
                    />
                </Grid2>
                <Grid2 size={{ xs: 12, lg: 3 }}>
                    <Stack
                        gap={2}
                        direction={{ xs: 'column', sm: 'row', lg: 'column' }}
                        sx={{
                            alignItems: { xs: 'normal', sm: 'end', lg: 'normal' },
                        }}
                    >
                        <Button variant="contained" onClick={handleOpenCreateDialog}>
                            <AddIcon />
                        </Button>
                        <Divider />
                        <FormControl>
                            <FormLabel>Стартовый вес</FormLabel>
                            <TextField
                                type='number'
                                variant="outlined"
                                value={dynamicStartedWeight}
                                onChange={handleChangeStartedWeight}
                            />
                        </FormControl>
                        <FormControl>
                            <FormLabel>Желанный вес</FormLabel>
                            <TextField
                                type='number'
                                variant="outlined"
                                value={dynamicDesiredWeight}
                                onChange={handleChangeDesiredWeight}
                            />
                        </FormControl>
                        <Stack direction="row" spacing={1}>
                            <Button
                                type="submit"
                                fullWidth
                                onClick={handleSetWorkoutSettings}
                                {...(!(dynamicStartedWeight && dynamicDesiredWeight) ? { disabled: true, variant: "outlined" } : { variant: "contained" })}
                            >
                                Сохранить
                            </Button>
                            <IconButton
                                sx={{ border: '1px solid' }}
                                onClick={handleResetWorkoutSettings}
                                {...(dynamicStartedWeight == staticStartedWeight && dynamicDesiredWeight == staticDesiredWeight ? { disabled: true } : {})}
                            >
                                <SyncIcon />
                            </IconButton>
                        </Stack>
                    </Stack>
                </Grid2>
            </Grid2>
            <Grid2 container rowSpacing={1} columns={12}>
                <Grid2 size={{ xs: 12, lg: 9 }}>
                    <TopBottomPagination
                        page={weightCurrentPage}
                        next_page={weightNextPage}
                        page_count={weightPageCount}
                        handleChangePage={handleChangePage}
                        handleShowMore={handleShowMore}
                    >
                        <TableContainer component={Paper}>
                            <Table
                                aria-label="simple table"
                                size='small'
                            >
                                <TableBody>
                                    {!weightList.length &&
                                        <Typography sx={{ m: 1 }}>
                                            {t('exercises_page.empty_table_message')}
                                        </Typography>
                                    }
                                    {weightList.map((weight_record, index) => (
                                        <>
                                            {getWeightTableYearRow(index)}
                                            <TableRow
                                                key={weight_record.id}
                                                sx={{
                                                    ...getStripedStyle(index),
                                                    ...getDeleteBottomBorderStyle(weight_record.description),
                                                }}
                                            >
                                                <TableCell scope="row">
                                                    <Typography variant="body1">
                                                        {getMonthDayDate(weight_record.date)}
                                                    </Typography>
                                                </TableCell>
                                                <TableCell scope="row">
                                                    <Stack direction="row" alignItems="center" gap={1}>
                                                        <Typography variant="body1">{parseFloat(weight_record.body_weight).toFixed(1)} кг</Typography>
                                                        {getWeightTrendingIcon(index)}
                                                    </Stack>
                                                </TableCell>
                                                <TableCell align='right' >
                                                    <IconButton size='small' onClick={() => handleOpenUpdateDialog(weight_record)}>
                                                        <EditIcon fontSize='small' />
                                                    </IconButton>
                                                </TableCell>
                                            </TableRow >
                                            {
                                                weight_record.description &&
                                                <TableRow sx={{ ...getStripedStyle(index) }}>
                                                    <TableCell colSpan={3}>
                                                        <Typography>{weight_record.description}</Typography>
                                                    </TableCell>
                                                </TableRow>
                                            }
                                        </>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </TopBottomPagination >
                </Grid2>
            </Grid2>
            <ChangeWeightDialog
                open={isUpdateDialogOpen}
                handleClose={handleCloseUpdateDialog}
                weightObject={changableWeightRecord}
                weightValue={changableWeightValueInput}
                weightDescription={changableWeightDescriptionInput}
                handleChangeWeightValue={e => setChangableWeightValueInput(e.target.value)}
                handleChangeWeightDescription={e => setChangableWeightDescriptionInput(e.target.value)}
                handleDelete={handleDeleteWeightRecord}
                handleSubmit={handleUpdateWeightRecord}
            />
            <CreateWeightDialog
                open={isCreateDialogOpen}
                weightDate={changableWeightDateInput}
                weightValue={changableWeightValueInput}
                weightDescription={changableWeightDescriptionInput}
                handleChangeWeightDate={value => setChangableWeightDateInput(value)}
                handleChangeWeightValue={e => setChangableWeightValueInput(e.target.value)}
                handleChangeWeightDescription={e => setChangableWeightDescriptionInput(e.target.value)}
                handleClose={handleCloseCreateDialog}
                handleSubmit={handleCreateWeightRecord}
            />
        </>
    );
}
