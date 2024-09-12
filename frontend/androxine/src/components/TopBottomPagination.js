import * as React from 'react';
import TablePagination from "@mui/material/TablePagination";
import Pagination from '@mui/material/Pagination';


export default function TopBottomPagination({ children }) {
    const [page, setPage] = React.useState(2);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    function PaginationInstance() {
        return (
            <TablePagination
                component="div"
                count={100}
                page={page}
                onPageChange={handleChangePage}
                rowsPerPage={rowsPerPage}
                onRowsPerPageChange={handleChangeRowsPerPage}
                // pageSizeOptions={[10, 20, 50]}
                autoHeight
                showFirstButton
                showLastButton
                sx={{
                }}
            />
        );
    };

    return (
        <>
            <PaginationInstance />
            {children}
            <PaginationInstance />

        </>
    );
}