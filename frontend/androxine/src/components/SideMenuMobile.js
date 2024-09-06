import * as React from 'react';
import PropTypes from 'prop-types';
import Drawer, { drawerClasses } from '@mui/material/Drawer';

import MenuContent from './MenuContent';

function SideMenuMobile({ open, toggleDrawer }) {
  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={toggleDrawer(false)}
      sx={{
        [`& .${drawerClasses.paper}`]: {
          backgroundImage: 'none',
          backgroundColor: 'background.paper',
        },
      }}
    >
      <MenuContent />
    </Drawer>
  );
}

SideMenuMobile.propTypes = {
  open: PropTypes.bool,
  toggleDrawer: PropTypes.func.isRequired,
};

export default SideMenuMobile;
