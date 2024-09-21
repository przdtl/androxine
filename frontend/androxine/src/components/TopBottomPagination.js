import * as React from 'react';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Pagination from '@mui/material/Pagination';


export default function TopBottomPagination({
    children,
    handleChangePage,
    page,
    page_count = 8,
    next_page = null,
}) {

    function PaginationInstance() {
        return (
            <Box sx={{
                display: 'flex',
                justifyContent: 'center',
            }}>
                <Pagination
                    count={page_count}
                    page={page}
                    onChange={handleChangePage}
                    sx={{
                        display: { md: 'block', xs: 'none' }
                    }}
                />
                <Pagination
                    siblingCount={0}
                    count={page_count}
                    page={page}
                    onChange={handleChangePage}
                    sx={{
                        display: { md: 'none', xs: 'block' }
                    }}
                />
            </Box>
        );
    };

    return (
        <>
            <PaginationInstance />
            {children}
            {next_page &&
                <Button
                    fullWidth
                >
                    Show more
                </Button>
            }
            <PaginationInstance />
        </>
    );
}