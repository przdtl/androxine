import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import { Grid2 } from '@mui/material';
import Search from "./Search";
import OutlinedInput from '@mui/material/OutlinedInput';
import Button from '@mui/material/Button';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};

export default function SearchFilter({ data }) {
    const handleClick = () => {
    };

    return (
        <>
            <Box
                // position="fixed"
                sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                <Box
                    sx={{
                        display: { xs: 'flex', sm: 'none' },
                        flexDirection: 'row',
                        gap: 1,
                        width: { xs: '100%', md: 'fit-content' },
                        overflow: 'auto',
                    }}
                >
                    <Search />
                    {/* <IconButton size="small" aria-label="RSS feed">
                        <SearchIcon />
                    </IconButton> */}
                </Box>
                <Box
                    sx={{
                        display: 'flex',
                        // flexDirection: { xs: 'column-reverse', md: 'row' },
                        // width: '100%',
                        // justifyContent: 'space-between',
                        // alignItems: { xs: 'start', md: 'center' },
                        gap: 4,
                        // overflow: 'auto',
                    }}
                >
                    {/* <Box
                        sx={{
                            display: 'inline-flex',
                            flexDirection: 'row',
                            gap: 3,
                            overflow: 'auto',
                        }}
                    > */}
                    {/* <Chip onClick={handleClick} size="medium" label="All categories" /> */}
                    {/* <Grid2
                        container
                        sx={{
                            gap: 3,
                            overflow: 'auto',
                        }}
                    > */}
                    <Box
                        sx={{
                            display: { xs: 'none', sm: 'flex' },
                            width: { xs: '100%', md: 'fit-content' },
                        }}>
                        <Search />
                    </Box>
                    <Box
                        sx={{
                            alignItems: 'center',
                            width: '100%',
                            display: 'flex',
                            justifyContent: { xs: 'space-between', md: 'start' },
                            // gap: 2,
                        }}
                    >
                        <FormControl sx={{ width: { xs: '100%', md: '35ch' }, m: 1 }}>
                            <InputLabel id="demo-multiple-chip-label">Category</InputLabel>
                            <Select
                                labelId="demo-multiple-chip-label"
                                id="demo-multiple-chip"
                                // value='hello'
                                // onChange={handleChange}
                                input={<OutlinedInput id="select-multiple-chip" label="Category" />}
                                MenuProps={MenuProps}
                            >
                                {data.map((item) => {
                                    return (
                                        <MenuItem MenuItem
                                            key={item.name}
                                            value={item.name}
                                        // style={getStyles(item.name, personName, theme)}
                                        >
                                            {item.name}
                                        </MenuItem>
                                    );
                                })}
                            </Select>
                        </FormControl>
                        <Button color="primary" variant="contained">
                            <SearchIcon />
                            Find
                        </Button>
                    </Box>
                    {/* {data.map((filter, index) => {
                            return (
                                <Grid2>
                                    <Chip
                                        size="large"
                                        onClick={handleClick}
                                        label={filter.name}
                                        sx={{
                                            backgroundColor: 'transparent',
                                            border: 'none',
                                        }}
                                    />
                                </Grid2>
                            );
                        })} */}
                    {/* </Grid2> */}
                    {/* </Box> */}
                    {/* <Box
                        sx={{
                            display: { xs: 'none', sm: 'flex' },
                            flexDirection: 'row',
                            gap: 1,
                            width: { xs: '100%', md: 'fit-content' },
                            overflow: 'auto',
                        }}
                    >
                        <Search />
                        <IconButton size="small" aria-label="RSS feed">
                            <SearchIcon />
                        </IconButton>
                    </Box> */}
                </Box>
            </Box >
        </>
    );
}