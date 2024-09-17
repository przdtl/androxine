import { useCallback } from "react"

import Box from "@mui/material/Box";
import Fab from "@mui/material/Fab";
import Zoom from "@mui/material/Zoom";
import { useScrollTrigger } from "@mui/material"
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
