import { useLocation } from 'react-router-dom';

import List from '@mui/material/List';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import Typography from '@mui/material/Typography';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListItemButton from '@mui/material/ListItemButton';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';

import LoginLogoutButton from './LoginLogoutButton';
// import Scale from '@mui/icons-material/Scale';
// import Calculate from '@mui/icons-material/Calculate';
// import Folder from '@mui/icons-material/Folder';
// import AssignmentInd from '@mui/icons-material/AssignmentInd';
// import FitnessCenter from '@mui/icons-material/FitnessCenter';
// import Event from '@mui/icons-material/Event';

const mainListItems = [
  { text: 'Home', icon: <HomeRoundedIcon />, href: '/home' },
  // { text: 'Exercises', icon: <FitnessCenter />, href: '/exercise' },
  // { text: 'Calculator', icon: <Calculate />, href: '/calculator' },
  // { text: 'Profile', icon: <AssignmentInd />, href: '/profile' },
  // { text: 'Templates', icon: <Folder />, href: '/template' },
  // { text: 'Workouts', icon: <Event />, href: '/workout' },
  // { text: 'Weight', icon: <Scale />, href: '/weight' },
];

const secondaryListItems = [
  { text: 'Settings', icon: <SettingsRoundedIcon />, href: '/settings' },
];

export default function MenuContent() {
  let location = useLocation();

  return (
    <>
      <Stack sx={{ flexGrow: 1 }}>
        <Stack sx={{ flexGrow: 1, p: 1, justifyContent: 'space-between' }}>
          <List dense>
            {mainListItems.map((item, index) => (
              <ListItem key={index} disablePadding sx={{ display: 'block' }}>
                <ListItemButton selected={item.href === location.pathname} href={item.href}>
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={<Typography variant="body1">{item.text}</Typography>} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
          <List dense>
            {secondaryListItems.map((item, index) => (
              <ListItem key={index} disablePadding sx={{ display: 'block' }}>
                <ListItemButton href={item.href}>
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={<Typography variant="body1">{item.text}</Typography>} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Stack>
        <Divider />
        <Stack sx={{ p: 2 }}>
          <LoginLogoutButton />
        </Stack>
      </Stack>
    </>
  );
}
