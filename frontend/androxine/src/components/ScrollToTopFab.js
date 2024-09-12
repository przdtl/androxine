import { useCallback } from "react"
import { useScrollTrigger } from "@mui/material"

import CssBaseline from '@mui/material/CssBaseline';
import Zoom from "@mui/material/Zoom";
import Box from "@mui/material/Box";
import Fab from "@mui/material/Fab";
import KeyboardArrowUp from '@mui/icons-material/KeyboardArrowUp';

export default function ScrollToTopFab() {
    const trigger = useScrollTrigger({
        threshold: 100,
        disableHysteresis: true,
    })

    const scrollToTop = useCallback(() => {
        window.scrollTo({ top: 0, behavior: "smooth" })
    }, [])

    return (
        <>
            <CssBaseline enableColorScheme />
            <Zoom in={trigger}>
                <Box
                    role="presentation"
                    sx={{
                        position: "fixed",
                        bottom: 32,
                        right: 32,
                        zIndex: 1,
                    }}
                >
                    <Fab
                        onClick={scrollToTop}
                        size="small"
                        aria-label="Scroll back to top"
                    >
                        <KeyboardArrowUp />
                    </Fab>
                </Box>
            </Zoom>
        </>
    );
}
