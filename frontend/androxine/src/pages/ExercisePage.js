import axios from 'axios';

import React, { useEffect } from 'react';

import { useSnackbar } from 'notistack'

import { useTranslation } from "react-i18next";

import { styled } from '@mui/material/styles';

import Chip from '@mui/material/Chip';
import Grid2 from '@mui/material/Grid2';
import Stack from '@mui/material/Stack';
import Table from '@mui/material/Table';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import TableRow from '@mui/material/TableRow';
import TableBody from '@mui/material/TableBody';
import TableHead from '@mui/material/TableHead';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import TableContainer from '@mui/material/TableContainer';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';

import SearchIcon from '@mui/icons-material/Search';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

import Search from '../components/Search';
import MultipleSelectChip from '../components/MultipleSelectChip';
import TopBottomPagination from "../components/TopBottomPagination";


const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.action.hover,
    },
    // hide last border
    '&:last-child td, &:last-child th': {
        border: 0,
    },
}));

const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
        backgroundColor: theme.palette.background.default,
        // color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
        fontSize: 14,
    },
}));

export default function ExercisePage() {
    const [categories, setCategories] = React.useState([]);
    const [exerciseList, setExerciseList] = React.useState([]);
    const [isAscendingNames, setIsAscendingNames] = React.useState(true);
    const [selectedCategories, setSelectedCategory] = React.useState([]);
    const [searchExerciseName, setSearchExerciseName] = React.useState('');
    const [exercisePageCount, setExercisePageCount] = React.useState(10);
    const [exerciseCurrentPage, setExerciseCurrentPage] = React.useState(1);
    const [exerciseNextPage, setExerciseNextPage] = React.useState(null);

    const { enqueueSnackbar } = useSnackbar();
    const { i18n, t } = useTranslation();

    const handleReorder = () => {
        setIsAscendingNames(!isAscendingNames);
    };

    const handleSearchChange = (event) => {
        setSearchExerciseName(event.target.value)
    };

    const handleSelectChange = (event) => {
        setSelectedCategory(event.target.value);
    };

    const handleChangePage = (event, value) => {
        setExerciseCurrentPage(value);
    };

    const handleGetCategories = () => {
        axios({
            url: 'http://127.0.0.1:8000/exercise/category/',
            method: 'get',
            headers: {
                "Content-Type": "application/json",
                "Accept-Language": i18n.language,
            },
        })
            .then(response => {
                console.log(response.data);
                setCategories(response.data.results);
            })
            .catch(error => {
                enqueueSnackbar(t('ошибка получения категорий'), {
                    variant: 'warning',
                    preventDuplicate: true,
                });
            });
    };

    const handleGetExercises = () => {
        axios({
            url: 'http://127.0.0.1:8000/exercise/',
            method: 'get',
            headers: {
                "Content-Type": "application/json",
                "Accept-Language": i18n.language,
            },
        })
            .then(response => {
                const data = response.data;
                setExerciseList(data.results);
                setExercisePageCount(data.total_pages);
                setExerciseNextPage(data.links.next);
            })
            .catch(error => {
                enqueueSnackbar(t('ошибка получения упражнений'), {
                    variant: 'warning',
                    preventDuplicate: true,
                });
            });
    };

    useEffect(() => {
        handleGetCategories();
        handleGetExercises();
    }, []);

    return (
        <>
            <h1>
                Exercises
            </h1>
            <Grid2
                container
                spacing={1}
                columns={18}
                justifyContent="end"
            >
                <Grid2 size={{ xs: 18, sm: 8, xl: 4 }}>
                    <Search
                        value={searchExerciseName}
                        handleChange={handleSearchChange}
                    />
                </Grid2>
                <Grid2 size={{ xs: 14, sm: 7, xl: 3 }}>
                    <MultipleSelectChip
                        value={selectedCategories}
                        items_list={categories}
                        handleChange={handleSelectChange}
                    />
                </Grid2>
                <Grid2 size={{ xs: 4, sm: 3, xl: 1 }}>
                    <Button
                        color="primary"
                        variant="contained"
                        sx={{ width: '100%' }}
                    >
                        <SearchIcon />
                        Find
                    </Button>
                </Grid2>
            </Grid2>
            <TopBottomPagination
                handleChangePage={handleChangePage}
                page={exerciseCurrentPage}
                next_page={exerciseNextPage}
                page_count={exercisePageCount}
            >
                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <StyledTableCell colSpan={2}>
                                    <Stack alignItems="center" direction="row" gap={2}>
                                        <Typography variant="body1">Название</Typography>
                                        <IconButton onClick={handleReorder} size="small">
                                            {isAscendingNames
                                                ? <ArrowUpwardIcon />
                                                : <ArrowDownwardIcon />
                                            }
                                        </IconButton>
                                    </Stack>
                                </StyledTableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {!exerciseList.length &&
                                <Typography>
                                    нет нхуя
                                </Typography>
                            }
                            {exerciseList.map((exercise) => (
                                <StyledTableRow
                                    key={exercise.name}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell component="th" scope="row">
                                        {exercise.name}
                                    </TableCell>
                                    <TableCell align="right">
                                        <Chip label={exercise.category} size='small' />
                                    </TableCell>
                                </StyledTableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </TopBottomPagination>
        </>
    );
}